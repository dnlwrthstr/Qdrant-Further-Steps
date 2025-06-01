#!/usr/bin/env python3
"""
Script to run the Qdrant Simple RAG API server.
"""
from qdrant_simple_rag.api import start

if __name__ == "__main__":
    print("Starting Qdrant Simple RAG API server on port 9080...")
    start()