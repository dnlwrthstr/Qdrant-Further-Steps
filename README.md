# Qdrant Vector Database Evaluation

This project evaluates and benchmarks different configurations of the Qdrant vector database, focusing on:
- Approximate Nearest Neighbor (ANN) search performance
- HNSW (Hierarchical Navigable Small World) parameter optimization
- Quantization settings
- Precision and performance metrics

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Installing Qdrant with Docker

You can easily run Qdrant in a Docker container:

```bash
docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)"/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

This command:
- Exposes the REST API port (6333) and the gRPC port (6334)
- Creates a persistent volume for your data in the `qdrant_storage` directory
- Uses the official Qdrant Docker image

Alternatively, you can use the scripts in the `scripts` directory to manage the Qdrant container:
- `scripts/install_qdrant.sh`: Pull the Qdrant Docker image
- `scripts/start_qdrant.sh`: Start the Qdrant container
- `scripts/stop_qdrant.sh`: Stop the Qdrant container
- `scripts/start_jupyter.sh`: Start the Jupyter notebook server
- `scripts/stop_jupyter.sh`: Stop the Jupyter notebook server
- `scripts/run_simple_rag_api.py`: Start the FastAPI server for the RAG functionality
- `scripts/start_frontend.sh`: Start only the frontend component (using npm)
- `scripts/start_rag_app.sh`: Start only the backend (shell script)
- `scripts/start_rag_app.py`: Start both the backend and frontend (Python script)

## Environment Setup

Create a `.env` file in your home directory with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
HF_API_KEY=your_huggingface_api_key
BASE_URL=your_base_url_if_needed
```

## Usage

### Running the Jupyter Notebook

You can start the Jupyter notebook server using the provided script:
```bash
./scripts/start_jupyter.sh
```

This script will:
- Check if Qdrant is running and start it if needed
- Verify all dependencies are installed
- Start the Jupyter notebook server

To stop the Jupyter server, you can either press Ctrl+C in the terminal or use:
```bash
./scripts/stop_jupyter.sh
```

Alternatively, you can start Jupyter manually:
```bash
jupyter notebook notebooks/quadrant_further_stps_1.ipynb
```

### Using the Python Package
```python
from qdrant_evaluation import (
    get_client, 
    load_environment, 
    evaluate_ann, 
    evaluate_hnsw_ef
)

# Load environment variables
env_vars = load_environment()

# Initialize Qdrant client
client = get_client(host="localhost", port=6333)

# Evaluate ANN search on a collection with embeddings
results = evaluate_ann(client, "your_collection_name", embeddings_dict)
print(f"Average precision: {results['avg_precision']}")
print(f"Average query time: {results['avg_query_time_ms']} ms")

# Evaluate different HNSW ef values
hnsw_results = evaluate_hnsw_ef(
    client, 
    "your_collection_name", 
    embeddings_dict, 
    hnsw_ef_values=[10, 20, 50, 100]
)
```

### Running the Example Script
The project includes an example script that demonstrates the basic functionality:

```bash
# Make sure you're in the project root directory
python examples/basic_evaluation.py
```

## Data Ingestion

The project includes a data ingestion utility for loading vector data into Qdrant collections.

### Using the DataIngestion Class

```python
from qdrant_data_ingestion.data_ingestion import DataIngestion

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
    file_path="path/to/your/data.json",
    collection_name="your_collection",
    vector_size=1536,
    distance=Distance.COSINE,
    hnsw_config=hnsw_config,
    show_progress=True
)

print(f"Ingested {total_points} points into collection")
```

### Using the Convenience Function

```python
from qdrant_data_ingestion.data_ingestion import ingest_from_file

# Ingest data using the convenience function
total_points = ingest_from_file(
    file_path="path/to/your/data.json",
    collection_name="your_collection",
    host="localhost",
    port=6333,
    grpc_port=6334,
    batch_size=1000,
    vector_size=1536,
    distance="cosine",  # Can use string instead of enum
    show_progress=True
)

print(f"Ingested {total_points} points into collection")
```

### Running the Data Ingestion Example

```bash
# Make sure you're in the project root directory
python examples/data_ingestion_example.py
```

## Retrieval-Augmented Generation (RAG) with Qdrant

This project includes a simple implementation of Retrieval-Augmented Generation (RAG) using Qdrant and OpenAI.

### What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that enhances large language models by:
1. Retrieving relevant information from a knowledge base (in this case, Qdrant vector database)
2. Augmenting the prompt to the language model with this retrieved context
3. Generating more accurate, up-to-date, and contextually relevant responses

### Using the RAG Functionality

The RAG implementation in this project allows you to ask questions and get answers based on documents stored in a Qdrant collection.

```python
from qdrant_simple_rag import ask_question

# Ask a question and get an answer
question = "What are the latest advancements in quantum computing?"
answer = ask_question(question, top_k=5)
print(answer)
```

### Running the RAG Example

```bash
# Make sure you're in the project root directory
python examples/simple_rag_example.py
```

This will run a demo with several example questions.

### Interactive CLI

You can also use the interactive CLI to ask questions:

```bash
python -m qdrant_simple_rag.simple_rag
```

### REST API

A FastAPI wrapper is available for accessing the RAG functionality via REST API:

```bash
# Start only the backend
./scripts/start_rag_app.sh

# Start both the backend and frontend together
./scripts/start_rag_app.py
# or
python scripts/start_rag_app.py
```

You can also run the backend and frontend separately:

```bash
# Start only the backend API
./scripts/run_simple_rag_api.py

# Start only the frontend (requires Node.js and npm)
./scripts/start_frontend.sh
```

Once the application is running, you can:
- Access the web interface at http://localhost:9080
- Access the API documentation at http://localhost:9090/docs
- Use the API endpoints:
  - GET `/`: Welcome message
  - POST `/ask`: Ask a question to the RAG system

Example with curl:
```bash
curl -X POST http://localhost:9090/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?", "top_k": 3}'
```

For more details, see the [API documentation](src/qdrant_simple_rag/README.md).

### Requirements for RAG

Before using the RAG functionality, make sure:
1. Qdrant is running (see "Installing Qdrant with Docker" section)
2. You have an OpenAI API key in your `.env` file
3. You have a collection in Qdrant with documents and their embeddings (the default collection name is "arxiv_papers")

## Project Structure
- `notebooks/`: Jupyter notebooks for interactive analysis
- `src/qdrant_evaluation/`: Python package with core functionality
  - `client.py`: Qdrant client setup and configuration
  - `embedding.py`: Embedding generation and test data loading
  - `evaluator.py`: Evaluation functions for different Qdrant configurations
  - `__init__.py`: Package exports and documentation
- `src/qdrant_data_ingestion/`: Python package for data ingestion
  - `data_ingestion.py`: Utilities for ingesting data into Qdrant
  - `__init__.py`: Package exports and documentation
- `src/qdrant_simple_rag/`: Python package for RAG functionality
  - `simple_rag.py`: Implementation of RAG using Qdrant and OpenAI
  - `api.py`: FastAPI wrapper for the RAG functionality
  - `README.md`: Documentation for the API
  - `__init__.py`: Package exports and documentation
- `examples/`: Example scripts demonstrating package usage
  - `basic_evaluation.py`: Basic example of evaluating Qdrant configurations
  - `data_ingestion_example.py`: Example of ingesting data into Qdrant
  - `simple_rag_example.py`: Example of using RAG functionality
- `tests/`: Test files for the project
  - `test_simple_rag_api.py`: Tests for the FastAPI wrapper
- `requirements.txt`: Project dependencies
- `setup.py`: Package installation configuration
