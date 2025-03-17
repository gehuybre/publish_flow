"""
Content Strategist agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class ContentStrategist(BaseAgent):
    """Agent responsible for developing content strategy for press releases."""
    
    def create_agent(self):
        """Create and return the Content Strategist agent."""
        return Agent(
            role="Content Strategist",
            goal="Develop a strategic framework for press releases by analyzing JSON data and user prompts",
            backstory="You are an expert Content Strategist with deep expertise in public relations and corporate communications.",
            verbose=True,
            allow_delegation=False,
            llm=self.create_llm(temperature=0.4),  # Lower temperature for more focused strategic thinking
        )