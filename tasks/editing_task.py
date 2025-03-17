"""
Editing task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class EditingTask(BaseTask):
    """Task for editing press release drafts."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the editing task.
        
        Args:
            agent: Editor agent to perform this task
            context_tasks: Must include the writing and fact checking tasks
            
        Returns:
            Task: A CrewAI task for editing press release drafts
        """
        if not context_tasks or len(context_tasks) < 2:
            raise ValueError("Editing task requires writing and fact checking tasks as context")
            
        write_drafts = context_tasks[0]
        fact_check = context_tasks[1]
        
        return Task(
            description=f"""
            Review and improve the provided press release drafts, considering the fact-checking reports.
            
            Focus on:
            - Strengthening the headline and lead paragraph
            - Ensuring the narrative flows logically
            - Verifying that key messages are prominently featured
            - Eliminating unnecessary jargon, redundancies, or vague statements
            - Balancing factual presentation with engaging style
            - Ensuring appropriate transitions between sections
            - Maintaining professional journalistic standards
            - Correcting any factual issues identified in the fact-checking reports
            
            Provide specific improvements with clear explanations for your reasoning.
            Submit complete revised versions of both drafts.
            
            Context: {self.context_str}
            
            Press release drafts: {{write_drafts.output}}
            Fact-checking reports: {{fact_check.output}}
            """,
            agent=agent,
            expected_output="Revised versions of both press release drafts with improved structure, clarity, and factual accuracy.",
            context=[write_drafts, fact_check]
        )