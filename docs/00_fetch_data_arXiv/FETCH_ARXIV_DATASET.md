# Fetching and Working with the arXiv Dataset (Version 85)

This guide explains how to download and prepare the arXiv dataset for building a simple natural language search engine.

## 📚 Project Overview

In this project, we will use a precompiled version of the arXiv dataset. Our goal is to enable users to find relevant scientific papers using a natural language query. This dataset contains metadata and precomputed embeddings for papers in fields such as mathematics, physics, and computer science.

## 📦 Dataset Details

- **Source**: [Kaggle](https://www.kaggle.com/)
- **Format**: `.zip` archive
- **Version**: `85`
- **Release Date**: `2024/12/22`
- **Estimated Size**: Large (may take a while to download)

## 📥 How to Download

1. Go to the [Kaggle dataset page](https://www.kaggle.com/) (replace with direct link if available).
2. Ensure you are logged in to your Kaggle account.
3. Locate **arXiv Dataset Version 85** (released on 2024/12/22).
4. Click **Download** to obtain the `.zip` file.
5. Extract the archive to your working directory:

   ```bash
   unzip arxiv-dataset-v85.zip -d ./arxiv_data
   ```

## 🗃️ Entry Structure

Each record in the dataset is stored in JSON format and has the following fields:

```json
{
  "id": "1706.03762",
  "submitter": "John Doe",
  "authors": "Alice Smith, Bob Johnson",
  "title": "An Interesting Paper",
  "comments": "Submitted to XYZ Conference",
  "journal-ref": "Journal of AI Research, 2023",
  "doi": "10.1000/j.jair.2023.123456",
  "report-no": "XYZ-2023-001",
  "categories": "cs.AI q-bio.NC",
  "license": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
  "abstract": "This paper explores ...",
  "versions": [
    {"version": "v1", "created": "2023-01-01"},
    {"version": "v2", "created": "2023-02-15"}
  ],
  "update_date": "2023-02-15",
  "authors_parsed": [["Smith", "Alice"], ["Johnson", "Bob"]],
  "embedding": [0.01234, -0.05678, ..., 0.09123] // 1536 floats
}
```

## 🧠 Embeddings

- The `embedding` field is a 1536-dimensional vector generated using OpenAI’s `text-embedding-ada-002` model.
- It is derived from an **augmented abstract**, which includes the original abstract, paper title, author names, and year.

## 🧪 Next Steps

After downloading and extracting the dataset:
- Load it into a script using `json` or `pandas` (if structured as JSON lines or tabular).
- Store documents in your search backend (e.g., Qdrant, OpenSearch, Weaviate).
- Use the embedding field to perform vector search.
- Optionally index metadata like title, authors, categories, and journal-ref for filtering.

```python
import json

with open('./arxiv_data/dataset.json', 'r') as f:
    data = json.load(f)

print(data[0]['title'])
print(data[0]['embedding'][:5])  # First 5 dimensions
```

## 📌 Notes

- Do not use older or newer versions of the dataset, as they might differ in structure or embedding generation.
- Ensure your vector database supports 1536-dimensional float vectors.
