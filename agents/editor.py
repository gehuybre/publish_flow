"""
Editor agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class Editor(BaseAgent):
    """Agent responsible for editing press release drafts."""
    
    def create_agent(self):
        """Create and return the Editor agent."""
        return Agent(
            role="Press Release Editor",
            goal="Review and refine drafts for structure, clarity, and messaging effectiveness",
            backstory="You are an experienced Press Release Editor with a keen eye for structure, clarity, and impact.",
            verbose=True,
            allow_delegation=True,
            llm=self.create_llm(),
        )