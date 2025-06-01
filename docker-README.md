# Containerized Qdrant Simple RAG Solution

This directory contains Docker configuration files to run the Qdrant Simple RAG solution in containers, connecting to an existing Qdrant instance.

## Components

The solution consists of two containerized components:

1. **Backend API**: Python FastAPI application that handles RAG queries
2. **Frontend**: Node.js Express application that provides a web interface

The solution connects to an existing Qdrant Vector Database that is already running in Docker.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Build and Start the Containers

```bash
docker-compose up -d
```

This will:
- Build the backend and frontend images
- Start the backend and frontend containers
- Connect to your existing Qdrant instance
- Set up the necessary network connections between them

### 2. Access the Application

- Frontend: http://localhost:9080
- Backend API: http://localhost:9090
- Qdrant API: Use your existing Qdrant instance (typically http://localhost:6333)

### 3. Stop the Containers

```bash
docker-compose down
```

Note: This will only stop the backend and frontend containers. Your existing Qdrant container will continue running.

## Configuration

### Environment Variables

The following environment variables can be configured in the docker-compose.yml file:

- **Backend**:
  - `QDRANT_HOST`: Hostname of the Qdrant server (default: "host.docker.internal", which connects to the host machine)
  - `QDRANT_PORT`: Port of the Qdrant server (default: 6333)
  - `OPENAI_API_KEY`: Your OpenAI API key

- **Frontend**:
  - `BACKEND_URL`: URL of the backend API (default: "http://backend:9090")
  - `PORT`: Port to run the frontend server on (default: 9080)

### Setting Up the OpenAI API Key

The application requires an OpenAI API key to function properly. There are several ways to provide this key:

1. **Using an environment variable (recommended)**:
   ```bash
   export OPENAI_API_KEY=your-openai-api-key
   docker-compose up -d
   ```
   This method passes your host machine's environment variable to the container.

2. **Using a .env file**:
   Create a `.env` file in the same directory as your docker-compose.yml:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```
   Then run:
   ```bash
   docker-compose up -d
   ```
   Docker Compose will automatically read variables from this file.

3. **Directly in docker-compose.yml (not recommended for production)**:
   You can hardcode the API key in the docker-compose.yml file, but this is not recommended for security reasons, especially in shared or version-controlled environments.

## Data Persistence

This configuration uses your existing Qdrant instance, so data persistence is managed by your existing Qdrant Docker container. The docker-compose.yml file in this project does not manage any Qdrant data volumes.

## Troubleshooting

### Connection Issues

If the frontend cannot connect to the backend, check:
1. That all containers are running (`docker-compose ps`)
2. That the backend container logs show no errors (`docker-compose logs backend`)
3. That the BACKEND_URL environment variable is set correctly in the docker-compose.yml file

### Qdrant Connection Issues

If the backend cannot connect to your existing Qdrant instance, check:
1. That your Qdrant container is running (`docker ps | grep qdrant`)
2. That your Qdrant container logs show no errors (`docker logs <your-qdrant-container-id>`)
3. That the QDRANT_HOST and QDRANT_PORT environment variables are set correctly in the docker-compose.yml file
4. If using host.docker.internal, ensure your Docker version supports this feature (Docker Desktop for Mac/Windows does, but some Linux Docker installations may require additional configuration)
5. If needed, you can use your host machine's actual IP address instead of host.docker.internal

### OpenAI API Key Issues

If you see errors related to the OpenAI API key, such as:
```
openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
```

Check:
1. That you've provided the OPENAI_API_KEY environment variable using one of the methods described in the "Setting Up the OpenAI API Key" section
2. That the API key is valid and has not expired
3. That the API key has the necessary permissions for the OpenAI models being used
4. You can verify the API key is being passed to the container by running: `docker-compose exec backend env | grep OPENAI`
