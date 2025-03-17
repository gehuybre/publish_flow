"""
Fact Checker agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class FactChecker(BaseAgent):
    """Agent responsible for verifying facts in press releases."""
    
    def create_agent(self):
        """Create and return the Fact Checker agent."""
        return Agent(
            role="Fact Checker",
            goal="Verify all facts, figures, and claims against the provided JSON data",
            backstory="You are a meticulous Fact-Checker with expertise in verifying information in media publications.",
            verbose=True,
            allow_delegation=False,
            llm=self.create_llm(temperature=0.2),  # Lower temperature for more precise fact-checking
        )