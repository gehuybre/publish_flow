"""
Press Release Writer agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class PressReleaseWriter(BaseAgent):
    """Agent responsible for writing press release drafts."""
    
    def create_agent(self):
        """Create and return the Press Release Writer agent."""
        return Agent(
            role="Press Release Writer",
            goal="Create compelling press release drafts based on strategic guidance and data",
            backstory="You are an expert Press Release Writer with years of experience crafting compelling announcements for organizations.",
            verbose=True,
            allow_delegation=True,
            llm=self.create_llm(),
        )