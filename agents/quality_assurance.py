"""
Quality Assurance agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class QualityAssurance(BaseAgent):
    """Agent responsible for assessing the quality of press releases."""
    
    def create_agent(self):
        """Create and return the Quality Assurance agent."""
        return Agent(
            role="Quality Assurance Specialist",
            goal="Evaluate press release versions against quality criteria and select the best output",
            backstory="You are a Quality Assurance Specialist with expertise in evaluating professional communications.",
            verbose=True,
            allow_delegation=False,
            llm=self.create_llm(temperature=0.3),  # Balanced temperature for evaluation
        )