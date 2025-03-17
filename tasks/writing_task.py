"""
Press release drafting task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class WritingTask(BaseTask):
    """Task for writing draft press releases."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the press release writing task.
        
        Args:
            agent: Press Release Writer agent to perform this task
            context_tasks: Must include the strategy development task
            
        Returns:
            Task: A CrewAI task for writing press release drafts
        """
        if not context_tasks or len(context_tasks) < 1:
            raise ValueError("Writing task requires strategy task as context")
            
        develop_strategy = context_tasks[0]
        
        return Task(
            description=f"""
            Create two distinct press release drafts based on the provided JSON data, user prompt, and strategic guidance.
            
            Your writing should:
            - Begin with a compelling headline and strong first paragraph that captures the essence of the news
            - Follow standard press release structure with dateline and appropriate formatting
            - Incorporate key data points from the JSON file accurately
            - Include at least one relevant quote from an appropriate stakeholder
            - End with standard boilerplate text and contact information
            - Match the recommended tone while maintaining journalistic standards
            - Be between 400-600 words unless otherwise specified
            
            Create press releases that journalists would find newsworthy and easy to report from.
            
            Context: {self.context_str}
            
            Strategic guidance: {{develop_strategy.output}}
            """,
            agent=agent,
            expected_output="Two distinct press release drafts that follow the strategic guidance.",
            context=[develop_strategy]
        )