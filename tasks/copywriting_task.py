"""
Copywriting enhancement task for press release enhancement.
"""
from typing import Dict, Any, Optional, List
from crewai import Task, Agent
from .task_base import BaseTask

class CopywritingTask(BaseTask):
    """Task for enhancing language in press releases."""
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return the copywriting enhancement task.
        
        Args:
            agent: Copywriter agent to perform this task
            context_tasks: Must include the editing task
            
        Returns:
            Task: A CrewAI task for enhancing press release language
        """
        if not context_tasks or len(context_tasks) < 1:
            raise ValueError("Copywriting task requires editing task as context")
            
        edit_drafts = context_tasks[0]
        
        return Task(
            description=f"""
            Enhance the language of the edited press release drafts for persuasiveness, engagement, and style
            while maintaining professional standards.
            
            Focus on:
            - Crafting more compelling headlines and subheadings
            - Strengthening the opening and closing paragraphs
            - Replacing generic phrases with more vivid, specific language
            - Ensuring consistent tone throughout the document
            - Enhancing quotes for memorability and impact
            - Improving sentence variety and paragraph transitions
            - Incorporating appropriate industry terminology
            - Maintaining conciseness while adding rhetorical strength
            
            Provide complete enhanced versions of both press releases with language improvements.
            
            Context: {self.context_str}
            
            Edited press release drafts: {{edit_drafts.output}}
            """,
            agent=agent,
            expected_output="Enhanced versions of both press releases with improved language, engagement, and persuasiveness.",
            context=[edit_drafts]
        )