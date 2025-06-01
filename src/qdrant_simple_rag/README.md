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

### Starting the Application

You can start the backend and frontend separately or together using the provided scripts:

#### Starting the Backend Only:

```bash
./scripts/start_rag_app.sh
```

Or:

```bash
python scripts/run_simple_rag_api.py
```

Or:

```bash
python -m qdrant_simple_rag.api
```

The backend API server will start on port 9090.

#### Starting the Frontend Only:

```bash
./scripts/start_frontend.sh
```

The frontend server will start on port 9080.

#### Starting Both Backend and Frontend:

```bash
./scripts/start_rag_app.py
```

Or:

```bash
python scripts/start_rag_app.py
```

When both are running:
- Backend API server runs on port 9090
- Frontend server runs on port 9080

You can access the frontend by opening a web browser and navigating to:

```
http://localhost:9080
```

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
curl http://localhost:9090/

# Ask a question
curl -X POST http://localhost:9090/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "top_k": 3}'
```

### Example Usage with Python

```python
import requests

# Base URL
base_url = "http://localhost:9090"

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

- Swagger UI: http://localhost:9090/docs
- ReDoc: http://localhost:9090/redoc
