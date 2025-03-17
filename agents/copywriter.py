"""
Copywriter agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class Copywriter(BaseAgent):
    """Agent responsible for enhancing language in press releases."""
    
    def create_agent(self):
        """Create and return the Copywriter agent."""
        return Agent(
            role="Copywriter",
            goal="Enhance language for persuasiveness and engagement while maintaining professional standards",
            backstory="You are an accomplished Copywriter specializing in polishing professional communications for impact and engagement.",
            verbose=True,
            allow_delegation=False,
            llm=self.create_llm(),
        )