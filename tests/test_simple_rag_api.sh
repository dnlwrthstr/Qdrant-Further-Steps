#!/bin/bash

# Script to test the simple_rag API in Docker installation
# Usage: ./test_simple_rag_api.sh [host] [port]
# Default host: localhost
# Default port: 9090

# Set default values
HOST=${1:-localhost}
PORT=${2:-9090}
BASE_URL="http://${HOST}:${PORT}"

echo "Testing simple_rag API at ${BASE_URL}"
echo "------------------------------------"

# Test the root endpoint
echo "1. Testing root endpoint..."
ROOT_RESPONSE=$(curl -s "${BASE_URL}/")
if [[ $ROOT_RESPONSE == *"Welcome to Qdrant Simple RAG API"* ]]; then
  echo "✅ Root endpoint test passed!"
  echo "Response: ${ROOT_RESPONSE}"
else
  echo "❌ Root endpoint test failed!"
  echo "Response: ${ROOT_RESPONSE}"
  exit 1
fi

echo ""

# Test the /ask endpoint
echo "2. Testing /ask endpoint..."
QUERY="What is Retrieval-Augmented Generation?"
echo "Sending query: '${QUERY}'"

ASK_RESPONSE=$(curl -s -X POST "${BASE_URL}/ask" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"${QUERY}\", \"top_k\": 3}")

if [[ $ASK_RESPONSE == *"answer"* ]]; then
  echo "✅ Ask endpoint test passed!"
  echo "Response:"
  echo "${ASK_RESPONSE}" | python -m json.tool 2>/dev/null || echo "${ASK_RESPONSE}"
else
  echo "❌ Ask endpoint test failed!"
  echo "Response: ${ASK_RESPONSE}"
  exit 1
fi

echo ""
echo "All tests completed successfully!"
echo ""
echo "Note: If you're running this against a Docker installation, make sure:"
echo "1. The Docker containers are running (docker-compose up -d)"
echo "2. If testing from outside the Docker network, use: ./test_simple_rag_api.sh localhost 9090"
echo "3. If testing from another container in the same network, use the service name: ./test_simple_rag_api.sh backend 9090"