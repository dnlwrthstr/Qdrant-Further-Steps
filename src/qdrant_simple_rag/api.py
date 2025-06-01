from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import the RAG functionality
from qdrant_simple_rag.simple_rag import ask_question

# Create FastAPI app
app = FastAPI(
    title="Qdrant Simple RAG API",
    description="A FastAPI wrapper for Qdrant Simple RAG",
    version="0.1.0",
)

# Define request model
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

# Define response model
class QueryResponse(BaseModel):
    answer: str

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Qdrant Simple RAG API"}

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Ask a question to the RAG system.
    
    Args:
        request: QueryRequest containing the query and optional top_k parameter
        
    Returns:
        QueryResponse containing the generated answer
    """
    try:
        answer = ask_question(request.query, request.top_k)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

def start():
    """Start the FastAPI server using uvicorn."""
    uvicorn.run("qdrant_simple_rag.api:app", host="0.0.0.0", port=9080, reload=True)

if __name__ == "__main__":
    start()