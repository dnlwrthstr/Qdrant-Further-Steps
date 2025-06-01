import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import the FastAPI app
from qdrant_simple_rag.api import app

# Create a test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns the expected welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Qdrant Simple RAG API"}

@patch("qdrant_simple_rag.api.ask_question")
def test_ask_endpoint_success(mock_ask_question):
    """Test the /ask endpoint with a successful query."""
    # Mock the ask_question function to return a predefined answer
    mock_ask_question.return_value = "This is a mocked answer."
    
    # Test data
    test_query = {"query": "What is RAG?", "top_k": 3}
    
    # Make the request
    response = client.post("/ask", json=test_query)
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"answer": "This is a mocked answer."}
    
    # Verify the mock was called with the correct arguments
    mock_ask_question.assert_called_once_with("What is RAG?", 3)

@patch("qdrant_simple_rag.api.ask_question")
def test_ask_endpoint_default_top_k(mock_ask_question):
    """Test the /ask endpoint with default top_k value."""
    # Mock the ask_question function
    mock_ask_question.return_value = "Answer with default top_k."
    
    # Test data with no top_k specified
    test_query = {"query": "What is RAG?"}
    
    # Make the request
    response = client.post("/ask", json=test_query)
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"answer": "Answer with default top_k."}
    
    # Verify the mock was called with the default top_k value (5)
    mock_ask_question.assert_called_once_with("What is RAG?", 5)

@patch("qdrant_simple_rag.api.ask_question")
def test_ask_endpoint_error(mock_ask_question):
    """Test the /ask endpoint when an error occurs."""
    # Mock the ask_question function to raise an exception
    mock_ask_question.side_effect = Exception("Test error")
    
    # Test data
    test_query = {"query": "What is RAG?"}
    
    # Make the request
    response = client.post("/ask", json=test_query)
    
    # Assertions
    assert response.status_code == 500
    assert "Error processing query: Test error" in response.json()["detail"]

def test_ask_endpoint_validation():
    """Test the /ask endpoint with invalid input."""
    # Test with missing required field
    response = client.post("/ask", json={"top_k": 3})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test with invalid type for top_k
    response = client.post("/ask", json={"query": "What is RAG?", "top_k": "invalid"})
    assert response.status_code == 422  # Unprocessable Entity