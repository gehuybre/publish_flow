import os
import sys
import importlib.util
import time

def ensure_directories(base_path):
    """
    Ensures all required directories exist.
    
    Args:
        base_path (str): Base directory path
    """
    directories = [
        f"{base_path}/prompts",
        f"{base_path}/prompts/special_instructions",
        f"{base_path}/user_input",
        f"{base_path}/data"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)

def import_module_from_file(file_path, module_name):
    """
    Imports a Python module from a file path.
    
    Args:
        file_path (str): Path to the Python file
        module_name (str): Name to give the module
        
    Returns:
        module: The imported module
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def main():
    """
    Main function to generate a press release and verify it.
    """
    # Configuration
    base_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow"
    
    # Ensure all directories exist
    ensure_directories(base_path)
    
    # Prompt user to select prompt file
    user_prompt_dir = f"{base_path}/user_input"
    prompt_files = [f for f in os.listdir(user_prompt_dir) if f.endswith(".txt")]
    
    if not prompt_files:
        print("Geen prompt bestanden gevonden in user_input directory.")
        return
    
    print("Beschikbare prompt bestanden:")
    for i, file in enumerate(prompt_files):
        print(f"{i+1}. {file}")
    
    try:
        selection = int(input("\nSelecteer een prompt bestand (nummer): ")) - 1
        if selection < 0 or selection >= len(prompt_files):
            print("Ongeldige selectie.")
            return
        
        selected_prompt = prompt_files[selection]
        print(f"\nGeselecteerde prompt: {selected_prompt}")
    except ValueError:
        print("Ongeldige invoer. Voer een nummer in.")
        return
    
    # Load the generate module
    generate_path = f"{base_path}/generate.py"
    if not os.path.exists(generate_path):
        print(f"Fout: generate.py niet gevonden op {generate_path}")
        return
    
    # Import the generate module
    generate_module = import_module_from_file(generate_path, "generate_module")
    
    # Generate press release
    print("\n" + "=" * 80)
    print("PERSBERICHT GENEREREN")
    print("=" * 80)
    
    start_time = time.time()
    output = generate_module.generate()
    end_time = time.time()
    
    print(f"\nPersbericht gegenereerd in {end_time - start_time:.2f} seconden.")
    
    # Verify the output
    verify_path = f"{base_path}/verify_output.py"
    if os.path.exists(verify_path):
        print("\n" + "=" * 80)
        print("PERSBERICHT VERIFIËREN")
        print("=" * 80)
        
        verify_module = import_module_from_file(verify_path, "verify_module")
        verify_module.run_verification(base_path)
    else:
        print("\nVerificatie overgeslagen: verify_output.py niet gevonden.")
    
    print("\n" + "=" * 80)
    print("PROCES VOLTOOID")
    print("=" * 80)
    print(f"Het gegenereerde persbericht is opgeslagen in: {base_path}/data/output.txt")

if __name__ == "__main__":
    main()