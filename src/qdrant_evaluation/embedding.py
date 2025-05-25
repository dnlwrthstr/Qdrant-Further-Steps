from openai import OpenAI
import os
from typing import Union, List
import json

def get_embedding(text: str) -> Union[List[float], None]:
    """
    Generate an embedding for the given text using OpenAI's API.
    
    Args:
        text (str): The text to generate an embedding for
        
    Returns:
        Union[List[float], None]: The embedding vector or None if an error occurs
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    client_qa = OpenAI(api_key=api_key)
    text = text.replace("\n", " ")
    try:
        response = client_qa.embeddings.create(input=[text], model="text-embedding-ada-002")
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def load_test_dataset(file_path="queries_embeddings.json") -> dict:
    """
    Load test dataset from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing test data
        
    Returns:
        dict: The loaded test dataset
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            test_dataset = json.load(file)
            return test_dataset
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: File {file_path} contains invalid JSON.")
        return {}