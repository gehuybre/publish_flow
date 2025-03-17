"""
HTML Formatter agent for the press release enhancement system.
"""
from crewai import Agent
from .agent_base import BaseAgent

class HTMLFormatter(BaseAgent):
    """Agent responsible for converting press releases to HTML format."""
    
    def create_agent(self):
        """Create and return the HTML Formatter agent."""
        return Agent(
            role="Web Design Specialist",
            goal="Transform final press release text into professionally formatted HTML",
            backstory="You are a Web Design Specialist focused on creating professional, responsive layouts for corporate communications.",
            verbose=True,
            allow_delegation=False,
            llm=self.create_llm(),
        )