import os
import re
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import original dependencies
# Import original dependencies - use the pattern from the working example
try:
    from google import genai
    from google.genai import types
    GOOGLE_API_AVAILABLE = True
except ImportError:
    print("Google GenerativeAI library not found - will use fallback methods")
    GOOGLE_API_AVAILABLE = False

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
    
    def __init__(self, base_path: str = "/content/drive/MyDrive/Colab Notebooks/publish_flow", debug: bool = False):
        """
        Initialize the Press Release Enhancement System.
        
        Args:
            base_path: Path to the directory containing data, prompts, and output files
            debug: Whether to enable debug mode with more verbose logging
        """
        # Set up paths
        self.base_path = Path(base_path)
        self.debug = debug
        
        if self.debug:
            print(f"Initializing Press Release Enhancement System with base path: {self.base_path}")
        
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
        
        # Set up Google AI client based on working example
        self.api_key = get_api_key('GEMINI_API_KEY')  # Try GEMINI_API_KEY
        if not self.api_key:
            self.api_key = get_api_key('AI_STUDIO_API')  # Fall back to AI_STUDIO_API
        
        if not self.api_key:
            raise ValueError("No API key available. Cannot initialize Google GenAI client.")
        
        if self.debug:
            print("API key loaded successfully.")
            
        # Initialize client using the working pattern
        if GOOGLE_API_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
                print("Successfully initialized Google GenAI client.")
                self.model = "gemini-2.0-flash"  # Default model for text generation
            except Exception as e:
                print(f"Error initializing Google GenAI client: {e}")
                self.client = None
        else:
            self.client = None
            print("Google GenAI library not available. Some features will be limited.")
        
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
        if self.debug:
            print("Creating specialized agents...")
        
        # Create agent instances
        content_strategist = ContentStrategist(self.api_key).create_agent()
        writer = PressReleaseWriter(self.api_key).create_agent()
        fact_checker = FactChecker(self.api_key).create_agent()
        editor = Editor(self.api_key).create_agent()
        copywriter = Copywriter(self.api_key).create_agent()
        quality_assurance = QualityAssurance(self.api_key).create_agent()
        html_formatter = HTMLFormatter(self.api_key).create_agent()
        
        agents = {
            "content_strategist": content_strategist,
            "writer": writer,
            "fact_checker": fact_checker,
            "editor": editor,
            "copywriter": copywriter,
            "quality_assurance": quality_assurance,
            "html_formatter": html_formatter
        }
        
        if self.debug:
            print(f"Created {len(agents)} agents: {', '.join(agents.keys())}")
        
        return agents
    
    def create_tasks(self, agents: Dict[str, Agent]) -> List[Task]:
        """Create and return all tasks for the crew workflow."""
        if self.debug:
            print("Creating workflow tasks...")
        
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
        
        tasks = [
            develop_strategy,
            write_drafts,
            fact_check,
            edit_drafts,
            enhance_language,
            quality_assessment,
            create_html
        ]
        
        if self.debug:
            print(f"Created {len(tasks)} tasks")
            for i, task in enumerate(tasks):
                task_name = task.__class__.__name__ if hasattr(task, "__class__") else "Task"
                assigned_agent = task.agent.role if hasattr(task, "agent") and hasattr(task.agent, "role") else "Unknown"
                print(f"Task {i+1}: {task_name} assigned to {assigned_agent}")
        
        return tasks
    
    def run_crew(self) -> str:
        """Run the full CrewAI workflow and return the final output."""
        try:
            # Verify that required data is available
            if not all([self.json_content, self.user_prompt, self.system_prompt]):
                print("Missing required data. Cannot proceed.")
                return None
            
            print("Creating agents for the press release crew...")
            try:
                agents = self.create_agents()
                print(f"Successfully created {len(agents)} agents: {list(agents.keys())}")
            except Exception as agent_error:
                print(f"Error creating agents: {agent_error}")
                raise
            
            print("Setting up workflow tasks...")
            try:
                tasks = self.create_tasks(agents)
                print(f"Successfully created {len(tasks)} tasks")
            except Exception as task_error:
                print(f"Error creating tasks: {task_error}")
                raise
            
            print("Assembling the crew...")
            try:
                crew = Crew(
                    agents=list(agents.values()),
                    tasks=tasks,
                    verbose=True,
                    process=Process.sequential
                )
                print("Successfully assembled crew.")
            except Exception as crew_error:
                print(f"Error assembling crew: {crew_error}")
                raise
            
            print("Starting the press release enhancement workflow...")
            try:
                result = crew.kickoff()
                print("Crew workflow completed successfully.")
            except Exception as kickoff_error:
                print(f"Error during crew kickoff: {kickoff_error}")
                raise
            
            # Extract the final HTML version
            self.final_version = result
            
            # Save the final output
            with open(self.paths["output"], "w", encoding="utf-8") as f:
                f.write(result)
            
            print(f"Output saved to {self.paths['output']}")
            
            # Print a preview of the result
            print("\nPress Release Preview (first 500 characters):")
            print("-" * 80)
            print(result[:500] + "..." if len(result) > 500 else result)
            print("-" * 80)
            
            return result
        except Exception as e:
            print(f"Critical error in run_crew(): {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_legacy(self) -> str:
        """
        Generate a press release using the original single-model approach.
        Updated to follow the working example pattern.
        """
        print("Generating press release using legacy method...")
        
        # Check if the client was initialized properly
        if not GOOGLE_API_AVAILABLE or not self.client:
            print("Google GenAI client not available. Using direct HTTP request instead.")
            return self._generate_with_direct_request()
        
        try:
            # Format the content based on the working example
            model = "gemini-2.0-flash"  # Text generation model
            
            # Combine JSON content and user prompt
            combined_prompt = f"{self.json_content}\n\n{self.user_prompt}"
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=combined_prompt),
                    ],
                ),
            ]
            
            # Create generation config
            generate_content_config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=64,
                max_output_tokens=8192,
                response_mime_type="text/plain",
            )
            
            # If system prompt is available, add it to the config
            if hasattr(types.GenerateContentConfig, 'system_instruction'):
                system_instruction = [types.Part.from_text(text=self.system_prompt)]
                generate_content_config.system_instruction = system_instruction
            
            print("Generating content with Google GenAI API...")
            output_text = ""
            
            # Use streaming to get the response in chunks
            for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                # Extract text from the chunk
                if hasattr(chunk, 'text'):
                    output_text += chunk.text
                    print(chunk.text, end="")
                # Handle different response formats
                elif hasattr(chunk, 'candidates') and chunk.candidates:
                    if chunk.candidates[0].content and chunk.candidates[0].content.parts:
                        for part in chunk.candidates[0].content.parts:
                            if hasattr(part, 'text') and part.text:
                                output_text += part.text
                                print(part.text, end="")
            
            print("\nContent generation complete.")
            
            # Save the output
            self._save_output(output_text)
            return output_text
            
        except Exception as e:
            print(f"Error generating content with Google GenAI API: {e}")
            print("Falling back to direct HTTP request...")
            return self._generate_with_direct_request()
    
    def _generate_with_direct_request(self) -> str:
        """
        Generate content using direct HTTP requests to the Google AI API.
        Used as a fallback when the client library fails.
        """
        try:
            import requests
            
            api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            # Combine JSON content and user prompt
            combined_prompt = f"{self.json_content}\n\n{self.user_prompt}"
            
            # Prepare the request payload
            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": combined_prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.95,
                    "topK": 64,
                    "maxOutputTokens": 8192
                }
            }
            
            # Add system instruction if available
            if self.system_prompt:
                # Insert system instruction before user content
                data["contents"].insert(0, {
                    "role": "system",
                    "parts": [{"text": self.system_prompt}]
                })
            
            print("Making direct HTTP request to Google AI API...")
            response = requests.post(api_url, headers=headers, json=data, timeout=180)
            
            if response.status_code == 200:
                result = response.json()
                try:
                    output_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    print("Successfully generated content with direct API request.")
                    
                    # Save the output
                    self._save_output(output_text)
                    return output_text
                except (KeyError, IndexError) as e:
                    print(f"Error extracting text from response: {e}")
                    print(f"Response structure: {result}")
                    raise
            else:
                print(f"API request failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                raise Exception(f"API request failed with status code {response.status_code}")
                
        except Exception as e:
            print(f"Failed to generate content with direct HTTP request: {e}")
            raise
    
    def _save_output(self, output_text: str) -> None:
        """Save the generated output to a file and print a preview."""
        if not output_text:
            print("WARNING: No output text was generated!")
            return
            
        with open(self.paths["output"], "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\nOutput saved to {self.paths['output']}")
        
        # Print a preview of the result
        print("\nPress Release Preview (first 500 characters):")
        print("-" * 80)
        print(output_text[:500] + "..." if len(output_text) > 500 else output_text)
        print("-" * 80)