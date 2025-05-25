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
- `examples/`: Example scripts demonstrating package usage
  - `basic_evaluation.py`: Basic example of evaluating Qdrant configurations
  - `data_ingestion_example.py`: Example of ingesting data into Qdrant
- `requirements.txt`: Project dependencies
- `setup.py`: Package installation configuration
