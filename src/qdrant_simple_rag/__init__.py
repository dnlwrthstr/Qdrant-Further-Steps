"""
Qdrant Simple RAG module for implementing Retrieval-Augmented Generation with Qdrant.

This module provides a simple implementation of RAG using Qdrant as the vector database
and OpenAI for generating answers based on retrieved context.
"""

from .simple_rag import ask_question, main

__all__ = ["ask_question", "main"]
