import os
import re
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import original dependencies
from google import genai
from google.genai import types

# Import API key helper function
from api_key_helper import get_api_key

# Import CrewAI dependencies
from crewai import Agent, Task, Crew, Process

# Import agent classes
from agents import (
    ContentStrategist,
    PressReleaseWriter,
    FactChecker,
    Editor,
    Copywriter,
    QualityAssurance,
    HTMLFormatter
)

# Import task classes
from tasks import (
    StrategyTask,
    WritingTask,
    FactCheckingTask,
    EditingTask,
    CopywritingTask,
    QualityAssessmentTask,
    HTMLFormattingTask
)

class PressReleaseEnhancementSystem:
    """
    A system for generating and enhancing press releases using a CrewAI-based 
    multi-agent approach with Google Generative AI models.
    """
    
    def __init__(self, base_path: str = "/content/drive/MyDrive/Colab Notebooks/publish_flow"):
        """
        Initialize the Press Release Enhancement System.
        
        Args:
            base_path: Path to the directory containing data, prompts, and output files
        """
        # Set up paths
        self.base_path = Path(base_path)
        self.paths = {
            "json": self.base_path / "data/emv_pers.json",
            "user_prompt": self.base_path / "user_input/prompt_1.txt",
            "system_prompt": self.base_path / "prompts/system_prompt.txt",
            "hyperlink_instructions": self.base_path / "prompts/hyperlink_requirements.txt",
            "special_instructions_dir": self.base_path / "prompts/special_instructions",
            "output": self.base_path / "data/output.txt",
            "drafts": self.base_path / "data/drafts"  # Directory to store draft versions
        }
        
        # Create drafts directory if it doesn't exist
        os.makedirs(self.paths["drafts"], exist_ok=True)
        
        # Set up Google AI client with flexible key handling
        self.api_key = get_api_key('AI_STUDIO_API')
        if not self.api_key:
            raise ValueError("No API key available. Cannot initialize Google GenAI client.")
        
        # Try different API patterns to handle different versions of the library
        try:
            # Try modern approach first
            self.client = genai.GenerativeModel(model_name="gemini-2.0-flash", api_key=self.api_key)
            print("Using newer Google Generative AI API")
        except AttributeError:
            try:
                # Try the older configure + Client approach
                genai.configure(api_key=self.api_key)
                self.client = genai.Client(api_key=self.api_key)
                print("Using older Google Generative AI API")
            except AttributeError:
                # If both fail, you might need to install the library
                print("Google Generative AI library not properly installed. Try: pip install google-generativeai")
                raise
        
        # Load essential data
        self.json_content = self._load_file(self.paths["json"])
        self.user_prompt = self._load_file(self.paths["user_prompt"])
        self.base_system_prompt = self._load_file(self.paths["system_prompt"])
        
        # Initialize data structures for the workflow
        self.strategy_document = None
        self.press_release_drafts = []
        self.fact_check_reports = []
        self.edited_versions = []
        self.copyedited_versions = []
        self.final_version = None
        self.html_version = None
        
        # Add special instructions based on topic
        self._add_topic_specific_instructions()
        
    def _load_file(self, file_path: Path) -> Optional[str]:
        """Load content from a file with error handling."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
    
    def _detect_topic_from_prompt(self, prompt_text: str) -> Optional[str]:
        """
        Detects the main topic from the prompt text to load appropriate special instructions.
        Returns the filename (without extension) of the special instruction file to use.
        """
        # Simple keyword-based topic detection
        if re.search(r'verkooprecht|registratierecht|belasting|fiscaal', prompt_text, re.IGNORECASE):
            return "tax_analysis"
        elif re.search(r'woonbeleid|betaalbaarheid|wonen|huisvesting', prompt_text, re.IGNORECASE):
            return "housing_policy"
        elif re.search(r'bouw|constructie|renovatie|verbouwing', prompt_text, re.IGNORECASE):
            return "construction"
        else:
            return None  # No special instructions needed
    
    def _add_topic_specific_instructions(self) -> None:
        """Add topic-specific instructions to the system prompt."""
        system_prompt = self.base_system_prompt
        
        # Add hyperlink instructions if available
        hyperlink_path = self.paths["hyperlink_instructions"]
        if hyperlink_path.exists():
            hyperlink_instructions = self._load_file(hyperlink_path)
            if hyperlink_instructions:
                system_prompt += "\n\n" + hyperlink_instructions
        
        # Detect topic and add special instructions
        if self.user_prompt:
            topic = self._detect_topic_from_prompt(self.user_prompt)
            if topic:
                special_instruction_path = self.paths["special_instructions_dir"] / f"{topic}.txt"
                if special_instruction_path.exists():
                    special_instructions = self._load_file(special_instruction_path)
                    if special_instructions:
                        system_prompt += "\n\n" + special_instructions
                        print(f"Applied special instructions for: {topic}")
        
        self.system_prompt = system_prompt
    
    def create_agents(self) -> Dict[str, Agent]:
        """Create and return all the specialized agents for the crew."""
        # Create agent instances
        content_strategist = ContentStrategist(self.api_key).create_agent()
        writer = PressReleaseWriter(self.api_key).create_agent()
        fact_checker = FactChecker(self.api_key).create_agent()
        editor = Editor(self.api_key).create_agent()
        copywriter = Copywriter(self.api_key).create_agent()
        quality_assurance = QualityAssurance(self.api_key).create_agent()
        html_formatter = HTMLFormatter(self.api_key).create_agent()
        
        return {
            "content_strategist": content_strategist,
            "writer": writer,
            "fact_checker": fact_checker,
            "editor": editor,
            "copywriter": copywriter,
            "quality_assurance": quality_assurance,
            "html_formatter": html_formatter
        }
    
    def create_tasks(self, agents: Dict[str, Agent]) -> List[Task]:
        """Create and return all tasks for the crew workflow."""
        
        # Assemble context data for tasks
        context_data = {
            "json_data": self.json_content,
            "user_prompt": self.user_prompt,
            "system_prompt": self.system_prompt
        }
        
        # Create task instances
        strategy_task_creator = StrategyTask(context_data)
        writing_task_creator = WritingTask(context_data)
        fact_checking_task_creator = FactCheckingTask(context_data)
        editing_task_creator = EditingTask(context_data)
        copywriting_task_creator = CopywritingTask(context_data)
        quality_assessment_task_creator = QualityAssessmentTask(context_data)
        html_formatting_task_creator = HTMLFormattingTask(context_data)
        
        # Create the actual task objects in sequence
        develop_strategy = strategy_task_creator.create_task(agents["content_strategist"])
        
        write_drafts = writing_task_creator.create_task(
            agents["writer"], 
            context_tasks=[develop_strategy]
        )
        
        fact_check = fact_checking_task_creator.create_task(
            agents["fact_checker"], 
            context_tasks=[write_drafts]
        )
        
        edit_drafts = editing_task_creator.create_task(
            agents["editor"], 
            context_tasks=[write_drafts, fact_check]
        )
        
        enhance_language = copywriting_task_creator.create_task(
            agents["copywriter"], 
            context_tasks=[edit_drafts]
        )
        
        quality_assessment = quality_assessment_task_creator.create_task(
            agents["quality_assurance"], 
            context_tasks=[enhance_language]
        )
        
        create_html = html_formatting_task_creator.create_task(
            agents["html_formatter"], 
            context_tasks=[quality_assessment]
        )
        
        return [
            develop_strategy,
            write_drafts,
            fact_check,
            edit_drafts,
            enhance_language,
            quality_assessment,
            create_html
        ]
    
    def run_crew(self) -> str:
        """Run the full CrewAI workflow and return the final output."""
        # Verify that required data is available
        if not all([self.json_content, self.user_prompt, self.system_prompt]):
            print("Missing required data. Cannot proceed.")
            return None
        
        print("Creating agents for the press release crew...")
        agents = self.create_agents()
        
        print("Setting up workflow tasks...")
        tasks = self.create_tasks(agents)
        
        print("Assembling the crew...")
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=2,
            process=Process.sequential  # Tasks must be executed in order
        )
        
        print("Starting the press release enhancement workflow...")
        result = crew.kickoff()
        
        # Extract the final HTML version
        self.final_version = result
        
        # Save the final output
        with open(self.paths["output"], "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"Output saved to {self.paths['output']}")
        return result
    
    def generate_legacy(self) -> str:
        """
        Generate a press release using the original single-model approach.
        Maintained for backward compatibility and comparison.
        Updated for different versions of the Google GenAI API.
        """
        print("Generating press release using legacy method...")
        
        # Handle different API versions
        try:
            # Newer API approach
            prompt = f"{self.json_content}\n\n{self.user_prompt}"
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 65536,
            }
            
            print("Generating press release with newer API...")
            
            response = self.client.generate_content(
                contents=[prompt],
                generation_config=generation_config,
                system_instruction=self.system_prompt
            )
            
            output_text = response.text
            
        except AttributeError:
            # Older API approach
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=self.json_content),
                        types.Part.from_text(text=self.user_prompt),
                    ],
                ),
            ]

            # Generate with the assembled system prompt
            generate_content_config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=64,
                max_output_tokens=65536,
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text=self.system_prompt),
                ],
            )

            model = "gemini-2.0-flash"
            output_text = ""
            
            print("Generating press release with older API...")
            for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                output_text += chunk.text
                print(chunk.text, end="")
            
            print()  # Add newline after streaming output
        
        if output_text:
            with open(self.paths["output"], "w", encoding="utf-8") as f:
                f.write(output_text)
            print(f"\nOutput saved to {self.paths['output']}")
        
        return output_text