"""
HTML formatting task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class HTMLFormattingTask(BaseTask):
    """Task for formatting press releases as HTML."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the HTML formatting task.
        
        Args:
            agent: HTML Formatter agent to perform this task
            context_tasks: Must include the quality assessment task
            
        Returns:
            Task: A CrewAI task for formatting press release as HTML
        """
        if not context_tasks or len(context_tasks) < 1:
            raise ValueError("HTML formatting task requires quality assessment task as context")
            
        quality_assessment = context_tasks[0]
        
        return Task(
            description=f"""
            Convert the final press release text into a well-structured HTML document with appropriate CSS styling.
            
            Your HTML/CSS implementation should:
            - Create a clean, professional layout appropriate for a press release
            - Include responsive design elements that work on mobile and desktop
            - Use appropriate typography for headlines, body text, and quotes
            - Structure the document with semantic HTML elements
            - Include proper spacing and visual hierarchy
            - Add appropriate metadata and SEO elements
            - Consider accessibility best practices
            
            Provide complete HTML and CSS code that can be directly implemented.
            
            Context: {self.context_str}
            
            Final press release: {{quality_assessment.output}}
            """,
            agent=agent,
            expected_output="Complete HTML and CSS code for the final press release with professional styling.",
            context=[quality_assessment]
        )