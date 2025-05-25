# BASICS OF VECTOR SEARCH

Vector search is a method of retrieving information based on the similarity between vector representations of data. It is commonly used in applications like search engines, recommendation systems, and natural language processing.

---

## 🔢 1. What Are Vectors?

A vector is a list of numbers representing features or characteristics of data. In vector search:

- **Dense Vector**: A short vector (e.g., 512 or 1536 dimensions) where most values are non-zero.
- **Sparse Vector**: A long vector (thousands to millions of dimensions) where most values are zero.

---

## 🔍 2. How Does Vector Search Work?

1. **Embed** your input (text, image, etc.) into a vector.
2. **Store** these vectors in a vector database (e.g., Qdrant, FAISS, Pinecone).
3. **Query** using a new input vector.
4. **Search** for similar vectors using a distance metric like cosine similarity or dot product.

---

## ⚙️ 3. Common Similarity Metrics

- **Cosine Similarity**: Measures the angle between vectors.
- **Dot Product**: Measures projection (used in many neural models).
- **Euclidean Distance**: Measures straight-line distance (not scale-invariant).

---

## 🧠 4. Example Use Cases

- **Semantic Search**: Search documents by meaning rather than keywords.
- **Recommendations**: Suggest items similar to user preferences.
- **Clustering & Classification**: Group similar items in high-dimensional space.
- **Multimodal Search**: Combine text, images, and metadata for richer queries.

---

## 🛠️ 5. Popular Tools & Libraries

| Tool       | Use Case                    |
|------------|-----------------------------|
| OpenAI     | Embedding generation        |
| Qdrant     | Vector database             |
| FAISS      | Fast vector similarity      |
| Pinecone   | Hosted vector search        |
| Weaviate   | Semantic search engine      |

---

## 🧪 6. Sample Workflow

```python
from openai import OpenAI
from qdrant_client import QdrantClient

# Generate vector
embedding = openai.embeddings.create(input="example query", model="text-embedding-ada-002")['data'][0]['embedding']

# Query vector DB
results = qdrant_client.query_points(
    collection_name="papers",
    query_vector=embedding,
    limit=5
)
```

---

## 📌 Summary

- Vector search enables semantic understanding of data.
- Dense vectors are used in modern ML embeddings.
- Vector similarity metrics allow fast and meaningful retrieval.
