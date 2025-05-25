#!/bin/bash

# Script to start the Jupyter notebook server

# Set environment variables if needed
export JUPYTER_PORT=8888
export JUPYTER_BASE_DIR="$(pwd)"
# Ensure the path is properly quoted for spaces

# Check if Qdrant is running, start if not
if ! curl -s http://localhost:6333/health >/dev/null; then
    echo "Qdrant is not running. Starting Qdrant..."
    ./scripts/start_qdrant.sh
    # Wait for Qdrant to be ready
    echo "Waiting for Qdrant to be ready..."
    sleep 5
fi

# Verify dependencies
echo "Checking dependencies..."
python -c "import qdrant_client, openai, dotenv, pandas, matplotlib" || {
    echo "Missing dependencies. Installing..."
    pip install -r requirements.txt
}

# Start Jupyter server
echo "Starting Jupyter server..."
echo "Jupyter notebook will be available at: http://localhost:$JUPYTER_PORT"
echo "To stop the Jupyter server, press Ctrl+C"

# Start Jupyter notebook server
jupyter notebook --port=$JUPYTER_PORT --notebook-dir="$JUPYTER_BASE_DIR"
