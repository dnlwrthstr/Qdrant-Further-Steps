FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY setup.py .
COPY README.md .

# Install the package in development mode
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 9090

# Command to run the application
CMD ["python", "-c", "import sys; from qdrant_simple_rag.api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=9090)"]
