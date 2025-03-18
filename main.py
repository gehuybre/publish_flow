"""
Main script to run the press release enhancement system.
"""
from press_release_system import PressReleaseEnhancementSystem

def main():
    base_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow"
    
    # Create with debug mode
    pr_system = PressReleaseEnhancementSystem(base_path=base_path, debug=True)
    
    print("System initialized. Ensuring we're using CrewAI...")
    
    # Explicit check to verify CrewAI method exists
    if not hasattr(pr_system, 'run_crew'):
        print("ERROR: run_crew method not found in PressReleaseEnhancementSystem class")
        raise AttributeError("run_crew method not found")
    
    # Force CrewAI mode
    print("Starting CrewAI execution...")
    result = pr_system.run_crew()  # No try/except to see the real error
    
    if not result:
        print("CrewAI execution returned empty result")
    
    print("CrewAI execution completed successfully")
    return result