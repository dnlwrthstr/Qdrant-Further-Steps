# BASICS_OF_VECTOR_SEARCH

This guide explains the fundamental difference between **dense vectors** and **sparse vectors**, two core representations used in vector search and machine learning.

---

## 🔵 Dense Vectors

**Definition**: A dense vector contains mostly non-zero values. Every element in the vector typically holds a meaningful value.

### ✅ Characteristics:
- **Compact** representation.
- Often used in **neural embeddings** (e.g., from BERT or `text-embedding-ada-002`).
- Size is usually fixed and small (e.g., 128, 512, 768, 1536 dimensions).
- Every dimension contributes to the meaning.

### 📌 Example:
```python
dense_vector = [0.21, -0.44, 0.01, 0.76, -0.59]
```

### 🧠 Used In:
- NLP embeddings (BERT, OpenAI, Word2Vec)
- Vector search (Qdrant, FAISS, Pinecone)
- Similarity search (cosine, dot product)

---

## ⚪ Sparse Vectors

**Definition**: A sparse vector contains mostly zeros. Only a small number of dimensions have non-zero values.

### ✅ Characteristics:
- Efficient to store in memory using **sparse formats** (like dictionaries or index-value pairs).
- Often used in **Bag-of-Words**, **TF-IDF**, or **one-hot** encodings.
- Size is usually **very large** (thousands to millions of dimensions).
- Most dimensions are irrelevant for a given input.

### 📌 Example:
```python
# Representing: {"feature_1234": 0.9, "feature_90512": 0.1}
sparse_vector = [0, 0, ..., 0, 0.9, ..., 0, 0.1, ..., 0]
```

### 🧠 Used In:
- Traditional ML models (e.g., logistic regression, SVM)
- Text classification with BoW/TF-IDF
- Information retrieval (inverted index search)

---

## 🔄 Summary Table

| Feature             | Dense Vector                          | Sparse Vector                          |
|---------------------|----------------------------------------|----------------------------------------|
| Dimensionality       | Low (e.g., 128–2048)                  | High (up to millions)                 |
| Value Distribution   | Mostly non-zero                      | Mostly zeros                          |
| Storage Format       | Array (standard)                     | Compressed (dict, CSR)                |
| Typical Usage        | Embeddings, deep learning            | Traditional ML, BoW/TF-IDF            |
| Efficiency (Search)  | Fast for vector similarity (ANN)     | Fast for exact match/inverted index   |
| Example Tools        | OpenAI, Qdrant, FAISS                | scikit-learn, Elasticsearch (TF-IDF)  |

---
