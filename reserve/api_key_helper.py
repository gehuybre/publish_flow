"""
Helper module for retrieving API keys from various sources.
"""

def get_api_key(key_name='AI_STUDIO_API'):
    """
    Get API key from various sources with graceful fallback.
    
    Tries multiple methods to retrieve the API key:
    1. Environment variables
    2. Colab userdata (if running in Colab)
    3. Local file (if exists)
    4. Manual input as a last resort
    
    Args:
        key_name: Name of the API key to retrieve
        
    Returns:
        str: The API key
    """
    import os
    
    # Method 1: Try environment variable
    api_key = os.environ.get(key_name)
    if api_key:
        print(f"API key found in environment variables.")
        return api_key
    
    # Method 2: Try Colab userdata if in Colab environment
    try:
        from google.colab import userdata
        try:
            api_key = userdata.get(key_name)
            if api_key:
                print(f"API key found in Colab userdata.")
                return api_key
        except Exception as e:
            print(f"Could not retrieve key from Colab userdata: {e}")
    except ImportError:
        print("Not running in Colab environment.")
    
    # Method 3: Try reading from a local key file
    key_file = os.path.expanduser(f"~/.{key_name.lower()}")
    try:
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                api_key = f.read().strip()
                if api_key:
                    print(f"API key found in local file: {key_file}")
                    return api_key
    except Exception as e:
        print(f"Could not read key file: {e}")
    
    # Method 4: Ask the user (last resort)
    print(f"\nNo {key_name} found in environment variables, Colab userdata, or local file.")
    api_key = input(f"Please enter your {key_name}: ").strip()
    
    # Optionally save for future use
    if api_key:
        save = input("Would you like to save this key for future use? (y/n): ").lower()
        if save == 'y':
            try:
                with open(key_file, 'w') as f:
                    f.write(api_key)
                os.chmod(key_file, 0o600)  # Secure permissions
                print(f"API key saved to {key_file}")
            except Exception as e:
                print(f"Could not save key: {e}")
    
    return api_key