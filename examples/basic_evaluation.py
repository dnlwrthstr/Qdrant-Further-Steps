#!/usr/bin/env python3
"""
Basic example of using the qdrant_evaluation package to evaluate
different Qdrant vector database configurations.
"""

import os
import sys
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.qdrant_evaluation import (
    get_client,
    get_embedding,
    evaluate_ann,
    evaluate_hnsw_ef,
    evaluate_ann_quantized,
    results_to_dataframe
)
from src.utils.environment import load_environment

def main():
    # Load environment variables
    env_vars = load_environment()
    print(f"Loaded environment variables: {', '.join(env_vars.keys())}")

    # Initialize Qdrant client
    client = get_client(host="localhost", port=6333)
    print("Connected to Qdrant server")

    # Collection name
    collection_name = 'arxiv_papers'

    # Load test dataset
    try:
        with open("queries_embeddings.json", 'r', encoding='utf-8') as file:
            embeddings = json.load(file)
            print(f"Loaded {len(embeddings)} embeddings from test dataset")
    except FileNotFoundError:
        print("Test dataset not found. Creating a sample embedding...")
        # Create a sample embedding if the dataset is not available
        sample_text = "This is a sample query for vector search evaluation"
        sample_embedding = get_embedding(sample_text)
        if sample_embedding:
            embeddings = {"sample_query": sample_embedding}
            print("Created sample embedding")
        else:
            print("Failed to create sample embedding. Please check your OpenAI API key.")
            return

    # Evaluate ANN search
    print("\nEvaluating ANN search...")
    ann_results = evaluate_ann(client, collection_name, embeddings)
    print(f"ANN Results: {ann_results}")

    # Evaluate HNSW ef parameter
    print("\nEvaluating HNSW ef parameter...")
    hnsw_ef_values = [10, 20, 50]
    hnsw_results = evaluate_hnsw_ef(client, collection_name, embeddings, hnsw_ef_values)

    # Convert results to DataFrame
    df = results_to_dataframe(hnsw_results)
    print("\nHNSW ef parameter evaluation results:")
    print(df)

    # Evaluate quantized search
    print("\nEvaluating quantized search...")
    quantized_results = evaluate_ann_quantized(client, collection_name, embeddings)
    print(f"Quantized Results: {quantized_results}")

if __name__ == "__main__":
    main()
