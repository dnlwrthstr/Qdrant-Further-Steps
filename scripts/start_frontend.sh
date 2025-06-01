#!/bin/bash

# Script to start the Qdrant Simple RAG frontend component

echo "Starting Qdrant Simple RAG frontend..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the repository root directory
cd "$SCRIPT_DIR/.."

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Change to the frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the frontend server
echo "Starting frontend server on port 9080..."
npm start

# Note: This script will keep running until you press Ctrl+C