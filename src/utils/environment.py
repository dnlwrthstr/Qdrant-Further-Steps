"""
Utility module for environment variable management.
This module provides functions to load and access environment variables.
"""

import os
from dotenv import load_dotenv

# Flag to track if environment has been loaded
_environment_loaded = False
# Dictionary to store environment variables
_environment_vars = {}

def load_environment():
    """
    Load environment variables from .env file.
    This function will only load the environment once, even if called multiple times.

    Returns:
        dict: Dictionary containing environment variables
    """
    global _environment_loaded, _environment_vars
    
    # Only load environment if it hasn't been loaded yet
    if not _environment_loaded:
        # Define paths for configuration files
        env_path = os.path.expanduser("~/.env")

        # Load environment variables from .env file
        load_dotenv(dotenv_path=env_path, override=True)

        # Read environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key":
            print("❌ Warning: OpenAI API key is missing or invalid. Please set the OPENAI_API_KEY environment variable.")

        # Store environment variables in the module-level dictionary
        _environment_vars = {
            "OPENAI_API_KEY": api_key,
            "HF_API_KEY": os.getenv("HF_API_KEY"),
            "BASE_URL": os.getenv("BASE_URL")
        }
        
        # Set the flag to indicate the environment has been loaded
        _environment_loaded = True
    
    return _environment_vars

def get_environment_variable(name, default=None):
    """
    Get a specific environment variable.
    If the environment hasn't been loaded yet, it will be loaded first.

    Args:
        name (str): Name of the environment variable
        default: Default value to return if the variable is not found

    Returns:
        The value of the environment variable, or the default value if not found
    """
    # Ensure environment is loaded
    if not _environment_loaded:
        load_environment()
    
    # Return the requested environment variable or default
    return _environment_vars.get(name, default)