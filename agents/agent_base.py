"""
Base agent class for press release enhancement system.
"""
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

class BaseAgent:
    """Base class for all agents in the press release system."""
    
    def __init__(self, api_key):
        """
        Initialize the base agent.
        
        Args:
            api_key: Google AI API key
        """
        self.api_key = api_key
    
    def create_llm(self, temperature=0.7):
        """Create a language model instance for this agent."""
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.api_key,
            temperature=temperature,
            top_p=0.95,
            top_k=64,
            max_output_tokens=4000,
        )
    
    def create_agent(self):
        """
        Create and return a CrewAI agent. 
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_agent()")