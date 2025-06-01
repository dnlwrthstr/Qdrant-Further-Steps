# Qdrant Simple RAG Frontend

This is the frontend component for the Qdrant Simple RAG application. It's a simple web application that allows users to ask questions and get answers powered by RAG technology.

## Prerequisites

- Node.js and npm installed on your system
- Backend API running on port 9090 (see instructions below)

## Running the Frontend

You can run the frontend in two ways:

### 1. Using the provided script

```bash
# From the repository root
./scripts/start_frontend.sh
```

### 2. Manually

```bash
# From the repository root
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:9080.

## Backend API

The frontend communicates with the backend API running on port 9090. Make sure the backend API is running before using the frontend.

To start the backend API:

```bash
# From the repository root
./scripts/run_simple_rag_api.py
```

## Architecture

The frontend is a simple web application that makes POST requests to the backend API endpoint at 'http://localhost:9090/ask'. The backend API processes the questions using RAG technology and returns answers.

The frontend consists of:
- HTML (index.html)
- CSS (styles.css)
- JavaScript (script.js)
- Node.js server (server.js)