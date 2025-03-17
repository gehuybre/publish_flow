"""
Fact checking task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class FactCheckingTask(BaseTask):
    """Task for verifying facts in press release drafts."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the fact checking task.
        
        Args:
            agent: Fact Checker agent to perform this task
            context_tasks: Must include the writing task
            
        Returns:
            Task: A CrewAI task for fact checking press release drafts
        """
        if not context_tasks or len(context_tasks) < 1:
            raise ValueError("Fact checking task requires writing task as context")
            
        write_drafts = context_tasks[0]
        
        return Task(
            description=f"""
            Verify all facts, figures, and claims in the provided press release drafts against the original JSON data.
            
            For each press release draft:
            - Identify every factual statement, number, date, name, and claim
            - Cross-reference each with the provided JSON data
            - Flag any discrepancies, inaccuracies, or unsubstantiated claims
            - Check for logical inconsistencies or misleading presentations of data
            - Verify that quotes are properly attributed
            - Ensure no critical information from the JSON is omitted
            
            Create a detailed fact-checking report for each draft highlighting any issues found and suggesting corrections.
            
            Context: {self.context_str}
            
            Press release drafts: {{write_drafts.output}}
            """,
            agent=agent,
            expected_output="Detailed fact-checking reports for each draft with identified issues and suggested corrections.",
            context=[write_drafts]
        )