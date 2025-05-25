from qdrant_client import QdrantClient, models
import os
from dotenv import load_dotenv

def get_client(host="localhost", port=6333):
    """
    Initialize and return a Qdrant client.
    
    Args:
        host (str): Qdrant server host
        port (int): Qdrant server port
        
    Returns:
        QdrantClient: Initialized Qdrant client
    """
    return QdrantClient(host=host, port=port)

def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        dict: Dictionary containing environment variables
    """
    # Define paths for configuration files
    env_path = os.path.expanduser("~/.env")
    
    # Load environment variables from .env file
    load_dotenv(dotenv_path=env_path, override=True)
    
    # Read environment variables
    return {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "HF_API_KEY": os.environ.get("HF_API_KEY"),
        "BASE_URL": os.environ.get("BASE_URL")
    }

def update_collection_config(client, collection_name, m=16, ef_construct=32):
    """
    Update HNSW configuration for a collection.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to update
        m (int): HNSW M parameter
        ef_construct (int): HNSW ef_construct parameter
    """
    client.update_collection(
        collection_name=collection_name,
        hnsw_config=models.HnswConfigDiff(m=m, ef_construct=ef_construct)
    )