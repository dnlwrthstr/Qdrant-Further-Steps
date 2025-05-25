#!/bin/bash

# Script to start the Qdrant container

# Check if the container already exists
if docker ps -a | grep -q "qdrant-container"; then
    echo "Qdrant container already exists. Starting existing container..."
    docker start qdrant-container
else
    echo "Creating and starting new Qdrant container..."
    # Create qdrant_storage directory if it doesn't exist
    mkdir -p "$(pwd)/qdrant_storage"
    
    # Run the container with the specified parameters
    docker run -d \
        --name qdrant-container \
        -p 6333:6333 \
        -p 6334:6334 \
        -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
        qdrant/qdrant
fi

echo "Qdrant container is now running."
echo "REST API is available at: http://localhost:6333"
echo "gRPC API is available at: localhost:6334"
echo "To stop the container, run: ./scripts/stop_qdrant.sh"