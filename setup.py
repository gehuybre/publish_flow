"""
Setup script for press release enhancement system.
Installs required dependencies and sets up the environment.
"""
import os
import sys
import subprocess
import argparse

def install_dependencies():
    """Install required Python packages."""
    print("Installing required dependencies...")
    
    # Base dependencies
    dependencies = [
        "google-generativeai",
        "crewai",
        "langchain-google-genai"
    ]
    
    # Install each dependency
    for dep in dependencies:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
    print("All dependencies installed successfully!")

def setup_directory_structure(base_path):
    """Create the required directory structure."""
    print(f"Setting up directory structure in {base_path}...")
    
    # Define directories to create
    directories = [
        "data",
        "user_input",
        "prompts",
        "prompts/special_instructions",
        "data/drafts"
    ]
    
    # Create each directory
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")

def create_placeholder_files(base_path):
    """Create placeholder files for required inputs."""
    print("Creating placeholder files...")
    
    # Define placeholder files
    placeholder_files = {
        "prompts/system_prompt.txt": "You are a professional PR writer tasked with writing high-quality press releases.",
        "user_input/prompt_1.txt": "Write a press release about the latest developments.",
        "prompts/hyperlink_requirements.txt": "Include hyperlinks to reference documents where appropriate."
    }
    
    # Create each placeholder file
    for file_path, content in placeholder_files.items():
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"Created placeholder file: {full_path}")
        else:
            print(f"File already exists: {full_path}")

def setup_environment_variable(api_key=None):
    """Set up environment variable for API key."""
    if api_key:
        os.environ['AI_STUDIO_API'] = api_key
        print("API key set as environment variable.")
        
        # Offer to save to a file for persistence
        save = input("Would you like to save this key to a file for future use? (y/n): ").lower()
        if save == 'y':
            key_file = os.path.expanduser(f"~/.ai_studio_api")
            try:
                with open(key_file, 'w') as f:
                    f.write(api_key)
                os.chmod(key_file, 0o600)  # Secure permissions
                print(f"API key saved to {key_file}")
            except Exception as e:
                print(f"Could not save key: {e}")
    else:
        print("No API key provided. You'll need to set this up later.")

def main():
    """Main function to set up the environment."""
    parser = argparse.ArgumentParser(description="Set up the press release enhancement system.")
    parser.add_argument("--base_path", default="/content/drive/MyDrive/Colab Notebooks/publish_flow",
                       help="Base path for the project")
    parser.add_argument("--api_key", help="Google AI API key")
    parser.add_argument("--skip_deps", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    # Print welcome message
    print("=" * 80)
    print("Press Release Enhancement System Setup")
    print("=" * 80)
    
    # Install dependencies
    if not args.skip_deps:
        install_dependencies()
    else:
        print("Skipping dependency installation.")
    
    # Setup directory structure
    setup_directory_structure(args.base_path)
    
    # Create placeholder files
    create_placeholder_files(args.base_path)
    
    # Setup environment variable
    setup_environment_variable(args.api_key)
    
    print("\nSetup completed successfully!")
    print("=" * 80)
    print(f"You can now run the system from directory: {args.base_path}")
    print("To use the system, run: python main.py")
    print("=" * 80)

if __name__ == "__main__":
    main()