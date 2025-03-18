#!/usr/bin/env python
"""
Quick installation script for Colab environment.
Run this first to install all dependencies.
"""

import os
import sys
import subprocess

def install_packages():
    """Install required packages"""
    print("Installing required packages...")
    
    # Install specific packages with versions
    packages = [
        "google-api-python-client",
        "google-generativeai",
        "crewai>=0.108.0",
        "langchain>=0.0.267",
        "langchain-google-genai>=0.0.5"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All packages installed successfully!")

def check_api_key():
    """Check if API key is set in environment variables"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        api_key = os.environ.get('AI_STUDIO_API')
    
    if not api_key:
        print("\n⚠️ WARNING: No API key found!")
        print("Please set your API key using one of these methods:")
        print("1. In Colab: from google.colab import userdata")
        print("   userdata.set('GEMINI_API_KEY', 'your_api_key_here')")
        print("2. In environment: os.environ['GEMINI_API_KEY'] = 'your_api_key_here'")
    else:
        print("\n✅ API key is set. You're ready to go!")

def main():
    """Main function to run setup"""
    print("Setting up Press Release Enhancement System...")
    
    # Install packages
    install_packages()
    
    # Import libraries to check they're installed correctly
    try:
        import google.generativeai as genai
        print(f"Successfully imported google.generativeai")
    except ImportError:
        print("WARNING: Failed to import google.generativeai")
    
    try:
        from google import genai as genai_alt
        print(f"Successfully imported google.genai")
    except ImportError:
        print("WARNING: Failed to import google.genai")
    
    try:
        import crewai
        print(f"Successfully imported crewai version {crewai.__version__}")
    except ImportError:
        print("WARNING: Failed to import crewai")
    
    # Check API key
    check_api_key()
    
    print("\nSetup complete! You can now run the system.")

if __name__ == "__main__":
    main()