#!/usr/bin/env python3
"""
Example script demonstrating the usage of the qdrant_simple_rag module.

This script shows how to use the RAG (Retrieval-Augmented Generation) functionality
provided by the qdrant_simple_rag module to answer questions based on a Qdrant collection.
"""

from qdrant_simple_rag import ask_question

def run_example():
    """
    Run a simple example of the RAG functionality.
    """
    print("🔍 Qdrant Simple RAG Example")
    print("----------------------------")
    
    # Example questions
    questions = [
        "What are the latest advancements in quantum computing?",
        "Explain the relationship between deep learning and neural networks.",
        "How does BERT work for natural language processing?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\nExample {i}: {question}")
        try:
            print("\nSearching and generating answer...")
            answer = ask_question(question)
            print("\n🧠 Answer:\n", answer)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Make sure Qdrant is running and the collection exists.")
    
    print("\n✅ Example completed!")
    print("To run the interactive CLI, use: python -m qdrant_simple_rag.simple_rag")

if __name__ == "__main__":
    run_example()