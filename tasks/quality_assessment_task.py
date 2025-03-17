"""
Quality assessment task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class QualityAssessmentTask(BaseTask):
    """Task for assessing quality of press releases."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the quality assessment task.
        
        Args:
            agent: Quality Assurance agent to perform this task
            context_tasks: Must include the copywriting task
            
        Returns:
            Task: A CrewAI task for assessing press release quality
        """
        if not context_tasks or len(context_tasks) < 1:
            raise ValueError("Quality assessment task requires copywriting task as context")
            
        enhance_language = context_tasks[0]
        
        return Task(
            description=f"""
            Assess both enhanced press release versions and determine which best meets quality standards
            or how elements from different versions might be combined.
            
            Evaluate each press release version against these criteria:
            - Headline effectiveness (attention-grabbing, clear, accurate)
            - Lead paragraph quality (answers who, what, when, where, why)
            - Message clarity (key points clearly communicated)
            - Structure and flow (logical progression, good transitions)
            - Language quality (engaging, professional, appropriate tone)
            - Factual accuracy (corresponds to provided JSON data)
            - Quote quality (adds value, sounds authentic)
            - Format adherence (follows press release conventions)
            
            Score each version on a scale of 1-10 for each criterion, providing specific comments.
            Then either select the best overall version OR create a combined optimal version
            using the strongest elements from both.
            
            Context: {self.context_str}
            
            Enhanced press release versions: {{enhance_language.output}}
            """,
            agent=agent,
            expected_output="Quality assessment of both versions with scores and comments, plus selection or creation of an optimal final version.",
            context=[enhance_language]
        )