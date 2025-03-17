"""
Base task class for press release enhancement system.
"""
from typing import Dict, List, Optional, Any
from crewai import Task, Agent

class BaseTask:
    """Base class for all tasks in the press release system."""
    
    def __init__(self, context_data: Dict[str, Any]):
        """
        Initialize the base task.
        
        Args:
            context_data: Dict containing json_data, user_prompt, and system_prompt
        """
        self.context_data = context_data
        self.context_str = str(context_data)  # Simple string conversion
    
    def create_task(self, agent: Agent, context_tasks: Optional[List[Task]] = None) -> Task:
        """
        Create and return a CrewAI task. 
        Must be implemented by subclasses.
        
        Args:
            agent: The CrewAI agent that will perform this task
            context_tasks: Optional list of tasks this task depends on
            
        Returns:
            Task: A CrewAI task instance
        """
        raise NotImplementedError("Subclasses must implement create_task()")