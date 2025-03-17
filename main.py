"""
Main script to run the press release enhancement system.
"""
from press_release_system import PressReleaseEnhancementSystem

def main():
    """Main function to run the press release enhancement system."""
    # Set the base path for your environment
    base_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow"
    
    # Create the press release system
    pr_system = PressReleaseEnhancementSystem(base_path=base_path)
    
    # Choose which approach to use
    use_crew_ai = True  # Set to False to use the legacy approach
    
    if use_crew_ai:
        result = pr_system.run_crew()
    else:
        result = pr_system.generate_legacy()
    
    return result


if __name__ == "__main__":
    main()