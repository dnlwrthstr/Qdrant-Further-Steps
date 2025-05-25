#!/bin/bash

# Script to stop the Qdrant container

# Check if the container exists and is running
if docker ps | grep -q "qdrant-container"; then
    echo "Stopping Qdrant container..."
    docker stop qdrant-container
    echo "Qdrant container has been stopped."
else
    # Check if the container exists but is not running
    if docker ps -a | grep -q "qdrant-container"; then
        echo "Qdrant container is not running."
    else
        echo "Qdrant container does not exist. Run install_qdrant.sh and start_qdrant.sh first."
    fi
fi

echo "To start the container again, run: ./scripts/start_qdrant.sh"