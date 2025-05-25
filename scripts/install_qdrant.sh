#!/bin/bash

# Script to install Qdrant Docker image

echo "Pulling the latest Qdrant Docker image..."
docker pull qdrant/qdrant

echo "Qdrant Docker image has been successfully pulled."
echo "To start the Qdrant container, run: ./scripts/start_qdrant.sh"