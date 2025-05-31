from qdrant_client import QdrantClient, models
import os
from utils.environment import load_environment, get_environment_variable

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
