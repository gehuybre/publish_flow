"""
Helper functions for API key management.
This module provides flexible ways to access API keys.
"""

import os
from pathlib import Path
import json

def get_api_key(key_name='GEMINI_API_KEY'):
    """
    Get API key from various sources with fallbacks.
    
    Args:
        key_name: Name of the environment variable to check
        
    Returns:
        str: The API key if found, None otherwise
    """
    # Check environment variables
    api_key = os.environ.get(key_name)
    if api_key:
        print(f"API key found in environment variables.")
        return api_key
    
    # Try alternate key names
    alternate_names = ['AI_STUDIO_API', 'GOOGLE_API_KEY', 'GEMINI_API_KEY']
    for name in alternate_names:
        if name != key_name:  # Skip the one we already checked
            api_key = os.environ.get(name)
            if api_key:
                print(f"API key found in {name} environment variable.")
                return api_key
    
    # Check for key in Colab userdata
    try:
        from google.colab import userdata
        api_key = userdata.get(key_name)
        if api_key:
            print(f"API key found in Colab userdata.")
            return api_key
    except (ImportError, AttributeError):
        pass  # Not running in Colab or userdata not available
    
    # Check for ~/.gemini_api_key file
    home_key_file = Path.home() / ".gemini_api_key"
    if home_key_file.exists():
        try:
            with open(home_key_file, "r") as f:
                api_key = f.read().strip()
                if api_key:
                    print(f"API key found in ~/.gemini_api_key file.")
                    return api_key
        except Exception:
            pass
    
    # Check for local .env file
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    if '=' in line:
                        k, v = line.strip().split('=', 1)
                        if k in alternate_names:
                            api_key = v.strip('"').strip("'")
                            if api_key:
                                print(f"API key found in .env file.")
                                return api_key
        except Exception:
            pass
    
    print(f"No API key found. Please set the {key_name} environment variable.")
    return None