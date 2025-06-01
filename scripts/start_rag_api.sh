#!/bin/bash

# Script to start the Qdrant Simple RAG API (backend only)
# The backend runs on port 9090 by default

echo "Starting Qdrant Simple RAG API server..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the repository root directory
cd "$SCRIPT_DIR/.."

# Function to handle script termination
function cleanup {
    echo "Stopping API server..."
    kill $BACKEND_PID 2>/dev/null
    echo "Qdrant Simple RAG API server has been stopped."
    exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Start the backend API server in the background
echo "Starting backend API server on port 9090..."
PYTHONPATH=$(pwd) python -c "import sys; from qdrant_simple_rag.api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=9090)" &
BACKEND_PID=$!

# Wait for user to press Ctrl+C
echo "Backend API server is running on port 9090. Press Ctrl+C to stop."
wait