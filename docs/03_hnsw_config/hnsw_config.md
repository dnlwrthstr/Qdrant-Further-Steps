# HNSW config

## Theory
In this stage, we will update the HNSW index. The HNSW algorithm constructs a multi-layer graph where each node represents a data vector, and edges represent connections to neighboring nodes. The graph enables efficient approximate nearest neighbor searches by navigating through these connections. The index setting happens in the hnsw_config in the Qdrant client methods:

```python
# default values
hnsw_config=models.HnswConfigDiff(
        m=16,
        ef_construct= 100
)
```

There are two main parameters: m (maximum connections), which defines the maximum number of outgoing connections (edges) each node can have in the lowest layer of the HNSW graph, and ef_construct (construction candidate list size), which controls the size of the dynamic list of nearest neighbor candidates considered during the index construction. Both m and ef_construct impact the speed of index construction, the memory consumption, the query speed, and the accuracy.

## Objectives
In this stage, you can reuse the precision and query time calculation function from the first stage. Here, we ask you to update the database index parameters 4 times and log their average precision and execution times after each indexing on the following values:

- m=8, ef_construct=50
- m=8, ef_construct=100
- m=16, ef_construct=32
- m=16, ef_construct=50

The index update can be performed with the .update_collection() method of the client:

```python
COLLECTION_NAME = 'arxiv_papers'

client.update_collection(
     collection_name=COLLECTION_NAME,
     hnsw_config=models.HnswConfigDiff()
)
```

## Results Analysis
Based on the obtained results, which parameter pair provides the fastest approximate search speed while keeping a high accuracy?

Select one option from the list:
- m=8, ef_construct=100
- m=16, ef_construct=32
- m=8, ef_construct=50
- m=16, ef_construct=50