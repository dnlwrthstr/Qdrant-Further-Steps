import os
from openai import OpenAI
from qdrant_client import QdrantClient
from utils.environment import load_environment, get_environment_variable

# Load environment variables
env_vars = load_environment()

# Configs
OPENAI_API_KEY = get_environment_variable("OPENAI_API_KEY", "your-openai-api-key")
COLLECTION_NAME = "arxiv_papers"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Get Qdrant connection details from environment variables or use defaults
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", 6333))

# Initialize clients
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(query: str, top_k=5):
    """
    Perform RAG (Retrieval-Augmented Generation) using Qdrant and OpenAI.

    Args:
        query (str): The user's question
        top_k (int): Number of documents to retrieve from Qdrant

    Returns:
        str: The generated answer
    """
    # Step 1: Embed user query
    response = openai_client.embeddings.create(
        input=[query],
        model=EMBEDDING_MODEL
    )
    query_vector = response.data[0].embedding

    # Step 2: Search Qdrant
    search_result = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    # Step 3: Prepare context from top-k matches
    context = "\n\n".join(
        hit.payload.get("title", "") + "\n" + hit.payload.get("abstract", "")
        for hit in search_result
    )

    # Step 4: Ask OpenAI using context
    system_prompt = "Use the following scientific context to answer the question."
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    """
    Main function to run the RAG example as a CLI application.
    """
    print("🔍 Qdrant Simple RAG Example")
    print("----------------------------")
    print(f"Using collection: {COLLECTION_NAME}")
    print(f"Using embedding model: {EMBEDDING_MODEL}")
    print("Type 'exit' to quit the application.")

    while True:
        q = input("\nAsk a scientific question (or type 'exit'): ")
        if q.lower() == "exit":
            break

        print("\nSearching and generating answer...")
        try:
            answer = ask_question(q)
            print("\n🧠 Answer:\n", answer)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
