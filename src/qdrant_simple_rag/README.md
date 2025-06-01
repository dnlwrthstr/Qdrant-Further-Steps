# Qdrant Simple RAG API

A FastAPI wrapper for the Qdrant Simple RAG system.

## Overview

This API provides a simple interface to the Qdrant Simple RAG (Retrieval-Augmented Generation) system. It allows you to ask questions and get answers based on the documents stored in the Qdrant vector database.

## Installation

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the API Server

To start the API server, run:

```bash
python -m qdrant_simple_rag.api
```

The server will start on port 9080 by default.

### API Endpoints

#### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message.
- **Response Example**:
  ```json
  {
    "message": "Welcome to Qdrant Simple RAG API"
  }
  ```

#### Ask Endpoint

- **URL**: `/ask`
- **Method**: `POST`
- **Description**: Ask a question to the RAG system.
- **Request Body**:
  ```json
  {
    "query": "What is RAG?",
    "top_k": 5  // Optional, defaults to 5
  }
  ```
- **Response Example**:
  ```json
  {
    "answer": "RAG (Retrieval-Augmented Generation) is a technique that combines retrieval-based and generation-based approaches for natural language processing tasks..."
  }
  ```

### Example Usage with curl

```bash
# Get welcome message
curl http://localhost:9080/

# Ask a question
curl -X POST http://localhost:9080/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "top_k": 3}'
```

### Example Usage with Python

```python
import requests

# Base URL
base_url = "http://localhost:9080"

# Get welcome message
response = requests.get(f"{base_url}/")
print(response.json())

# Ask a question
query_data = {
    "query": "What is RAG?",
    "top_k": 3
}
response = requests.post(f"{base_url}/ask", json=query_data)
print(response.json())
```

## Testing

To run the tests for the API, use pytest:

```bash
pytest tests/test_simple_rag_api.py
```

## API Documentation

When the server is running, you can access the auto-generated API documentation at:

- Swagger UI: http://localhost:9080/docs
- ReDoc: http://localhost:9080/redoc