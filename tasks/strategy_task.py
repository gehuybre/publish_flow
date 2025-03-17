"""
Strategic framework development task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class StrategyTask(BaseTask):
    """Task for developing a strategic framework for press releases."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the strategy development task.
        
        Args:
            agent: Content Strategist agent to perform this task
            context_tasks: Not used for this initial task
            
        Returns:
            Task: A CrewAI task for strategic framework development
        """
        return Task(
            description=f"""
            Analyze the provided JSON data and user prompt to develop a strategic framework for this press release.
            
            Important considerations:
            - Identify 3-5 key messages that should be highlighted
            - Determine the most newsworthy angle based on the data
            - Identify the target audience and their interests
            - Recommend tone and style appropriate for this press release (formal, conversational, technical)
            - Suggest a narrative structure that will best serve the content
            
            Your output should provide clear strategic guidance that a writer can follow to create an effective press release.
            Include reasoning for your recommendations.
            
            Context: {self.context_str}
            """,
            agent=agent,
            expected_output="A comprehensive strategic framework document with key messages, angle, audience analysis, tone recommendations, and narrative structure guidance."
        )