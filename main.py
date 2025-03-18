"""
Main script to run the press release enhancement system.
"""
import argparse
import os
from press_release_system import PressReleaseEnhancementSystem

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Press Release Enhancement System')
    parser.add_argument('--base_path', type=str, 
                        default="/content/drive/MyDrive/Colab Notebooks/publish_flow",
                        help='Base path for the project directory')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--api_key', type=str,
                        help='Optional API key (otherwise reads from environment)')
    args = parser.parse_args()
    
    # Set API key if provided
    if args.api_key:
        os.environ['AI_STUDIO_API'] = args.api_key
        print("Using API key from command line arguments")
    
    # Print CrewAI version for debugging
    try:
        import crewai
        print(f"CrewAI version: {crewai.__version__}")
    except (ImportError, AttributeError):
        print("Unable to determine CrewAI version")
    
    print(f"Starting Press Release Enhancement System with base path: {args.base_path}")
    
    # Create system with debug mode
    pr_system = PressReleaseEnhancementSystem(base_path=args.base_path, debug=args.debug)
    
    print("System initialized. Running with CrewAI multi-agent workflow...")
    
    # Execute the CrewAI workflow
    try:
        result = pr_system.run_crew()
        if not result:
            print("WARNING: CrewAI execution returned empty result")
        else:
            print("CrewAI execution completed successfully!")
            return result
    except Exception as e:
        print(f"ERROR in CrewAI execution: {e}")
        import traceback
        traceback.print_exc()
        print("\nAttempting fallback to legacy mode...")
        
        # Only try legacy as fallback
        try:
            result = pr_system.generate_legacy()
            if result:
                print("Legacy generation completed successfully")
                return result
            else:
                print("Legacy generation failed")
                return None
        except Exception as legacy_error:
            print(f"ERROR in legacy execution: {legacy_error}")
            return None

if __name__ == "__main__":
    main()