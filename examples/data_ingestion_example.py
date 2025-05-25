"""
Example script demonstrating how to use the qdrant_data_ingestion package.

This script shows two ways to ingest data into Qdrant:
1. Using the DataIngestion class directly
2. Using the convenience function ingest_from_file
"""

import os
from qdrant_client.models import Distance

from qdrant_data_ingestion.data_ingestion import DataIngestion, ingest_from_file

# Example file path - replace with your actual data file
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                         "data", "ml-arxiv-embeddings.json")

# Example 1: Using the DataIngestion class directly
def example_using_class():
    print("Example 1: Using DataIngestion class directly")
    
    # Initialize the DataIngestion class
    ingestion = DataIngestion(
        host="localhost",
        port=6333,
        grpc_port=6334,
        batch_size=1000
    )
    
    # Configure HNSW index (optional)
    hnsw_config = {
        "m": 16,
        "ef_construct": 100
    }
    
    # Ingest data
    total_points = ingestion.ingest_data(
        file_path=DATA_FILE,
        collection_name="arxiv_papers_example1",
        vector_size=1536,
        distance=Distance.COSINE,
        hnsw_config=hnsw_config,
        show_progress=True
    )
    
    print(f"Ingested {total_points} points into collection 'arxiv_papers_example1'")

# Example 2: Using the convenience function
def example_using_function():
    print("\nExample 2: Using convenience function")
    
    # Ingest data using the convenience function
    total_points = ingest_from_file(
        file_path=DATA_FILE,
        collection_name="arxiv_papers_example2",
        host="localhost",
        port=6333,
        grpc_port=6334,
        batch_size=1000,
        vector_size=1536,
        distance="cosine",  # Can use string instead of enum
        show_progress=True
    )
    
    print(f"Ingested {total_points} points into collection 'arxiv_papers_example2'")

if __name__ == "__main__":
    print(f"Looking for data file at: {DATA_FILE}")
    if os.path.exists(DATA_FILE):
        example_using_class()
        example_using_function()
    else:
        print(f"Data file not found at {DATA_FILE}")
        print("Please update the DATA_FILE path to point to your actual data file.")