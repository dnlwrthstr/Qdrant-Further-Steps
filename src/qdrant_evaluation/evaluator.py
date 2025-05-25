from qdrant_client import QdrantClient, models
import time
from typing import List, Set, Dict, Tuple
import pandas as pd

def precision_k(ann_results: Set, exact_results: Set, k: int = 10) -> float:
    """
    Calculate precision@k metric.
    
    Args:
        ann_results (Set): Set of IDs from approximate nearest neighbor search
        exact_results (Set): Set of IDs from exact k-NN search
        k (int): Number of results to consider
        
    Returns:
        float: Precision@k value
    """
    return len(ann_results.intersection(exact_results)) / k

def get_ann_points(client: QdrantClient, collection_name: str, embedding: List, k: int = 10) -> Tuple[List, float]:
    """
    Get approximate nearest neighbor points.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embedding (List): Query embedding vector
        k (int): Number of results to return
        
    Returns:
        Tuple[List, float]: List of result IDs and query execution time
    """
    start_time_ann = time.time()
    ann_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=k
    ).points
    ann_time = time.time() - start_time_ann
    ids = [res.payload['id'] for res in ann_result]
    return ids, ann_time

def get_hnsw_points(client: QdrantClient, collection_name: str, embedding: List, hnsw_ef: int, k: int = 10) -> Tuple[List, float]:
    """
    Get HNSW search results with specific ef parameter.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embedding (List): Query embedding vector
        hnsw_ef (int): HNSW ef search parameter
        k (int): Number of results to return
        
    Returns:
        Tuple[List, float]: List of result IDs and query execution time
    """
    start_time_hnsw = time.time()
    hnsw_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=k,
        search_params=models.SearchParams(hnsw_ef=hnsw_ef)
    ).points
    hnsw_time = time.time() - start_time_hnsw
    ids = [res.payload['id'] for res in hnsw_result]
    return ids, hnsw_time

def get_knn_points(client: QdrantClient, collection_name: str, embedding: List, k: int = 10) -> Tuple[List, float]:
    """
    Get exact k-NN search results.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embedding (List): Query embedding vector
        k (int): Number of results to return
        
    Returns:
        Tuple[List, float]: List of result IDs and query execution time
    """
    start_time_knn = time.time()
    knn_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=k,
        search_params=models.SearchParams(exact=True),
    ).points
    knn_time = time.time() - start_time_knn
    ids = [res.payload['id'] for res in knn_result]
    return ids, knn_time

def get_ann_points_quantized(client: QdrantClient, collection_name: str, embedding: List, k: int = 10) -> Tuple[List, float]:
    """
    Get approximate nearest neighbor points with quantization.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embedding (List): Query embedding vector
        k (int): Number of results to return
        
    Returns:
        Tuple[List, float]: List of result IDs and query execution time
    """
    start_time_ann = time.time()
    ann_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=k,
        search_params=models.SearchParams(
            quantization=models.QuantizationSearchParams(
                rescore=False,
                oversampling=2.0,
            )
        )
    ).points
    ann_time = time.time() - start_time_ann
    ids = [res.payload['id'] for res in ann_result]
    return ids, ann_time

def get_knn_points_ignoring_quantization(client: QdrantClient, collection_name: str, embedding: List, k: int = 10) -> Tuple[List, float]:
    """
    Get exact k-NN search results ignoring quantization.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embedding (List): Query embedding vector
        k (int): Number of results to return
        
    Returns:
        Tuple[List, float]: List of result IDs and query execution time
    """
    start_time_knn = time.time()
    knn_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=k,
        search_params=models.SearchParams(
            quantization=models.QuantizationSearchParams(ignore=True)
        ),
    ).points
    knn_time = time.time() - start_time_knn
    ids = [res.payload['id'] for res in knn_result]
    return ids, knn_time

def evaluate_ann(client: QdrantClient, collection_name: str, embeddings: Dict) -> Dict:
    """
    Evaluate ANN search performance.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embeddings (Dict): Dictionary of embeddings to evaluate
        
    Returns:
        Dict: Evaluation results
    """
    ann_results = [get_ann_points(client, collection_name, vector) for _, vector in embeddings.items()]
    knn_results = [get_knn_points(client, collection_name, vector) for _, vector in embeddings.items()]

    results = [(precision_k(set(ann_id_list), set(knn_id_list)), ann_execution_time)
               for (ann_id_list, ann_execution_time), (knn_id_list, knn_execution_time)
               in zip(ann_results, knn_results)]

    precisions, exec_time = zip(*results)
    avg_precision = sum(precisions) / len(precisions)
    avg_query_time_ms = sum(exec_time) / len(exec_time) * 1000

    return {
        "avg_precision": avg_precision,
        "avg_query_time_ms": avg_query_time_ms
    }

def evaluate_hnsw_ef(client: QdrantClient, collection_name: str, embeddings: Dict, hnsw_ef_values: List[int] = None) -> List[Dict]:
    """
    Evaluate HNSW ef parameter performance.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embeddings (Dict): Dictionary of embeddings to evaluate
        hnsw_ef_values (List[int]): List of ef values to evaluate
        
    Returns:
        List[Dict]: Evaluation results for each ef value
    """
    if hnsw_ef_values is None:
        hnsw_ef_values = [10, 20, 50, 100, 200]
    
    knn_results = [get_knn_points(client, collection_name, vector) for _, vector in embeddings.items()]

    results_list = []
    for hnsw_ef in hnsw_ef_values:
        hnsw_results = [get_hnsw_points(client, collection_name, vector, hnsw_ef) for _, vector in embeddings.items()]

        result_hnsw = [
            (precision_k(set(hnsw_id_list), set(knn_id_list)), hnsw_execution_time)
            for (hnsw_id_list, hnsw_execution_time), (knn_id_list, knn_execution_time)
            in zip(hnsw_results, knn_results)]

        prec, hnsw_exe_time = zip(*result_hnsw)
        avg_precision = sum(prec) / len(prec)
        avg_query_time_ms = sum(hnsw_exe_time) / len(hnsw_exe_time) * 1000

        results_list.append({
            "hnsw_ef": hnsw_ef,
            "avg_precision": avg_precision,
            "avg_query_time_ms": avg_query_time_ms
        })

    return results_list

def evaluate_ann_quantized(client: QdrantClient, collection_name: str, embeddings: Dict) -> Dict:
    """
    Evaluate ANN search performance with quantization.
    
    Args:
        client (QdrantClient): Qdrant client
        collection_name (str): Name of the collection to query
        embeddings (Dict): Dictionary of embeddings to evaluate
        
    Returns:
        Dict: Evaluation results
    """
    ann_results = [get_ann_points_quantized(client, collection_name, vector) for _, vector in embeddings.items()]
    knn_results = [get_knn_points_ignoring_quantization(client, collection_name, vector) for _, vector in embeddings.items()]

    results = [(precision_k(set(ann_id_list), set(knn_id_list)), ann_execution_time)
               for (ann_id_list, ann_execution_time), (knn_id_list, knn_execution_time)
               in zip(ann_results, knn_results)]

    precisions, exec_time = zip(*results)
    avg_precision = sum(precisions) / len(precisions)
    avg_query_time_ms = sum(exec_time) / len(exec_time) * 1000

    return {
        "avg_precision": avg_precision,
        "avg_query_time_ms": avg_query_time_ms
    }

def compute_avg_metrics(data: List[Dict]) -> Dict[str, float]:
    """
    Compute the average of all keys starting with 'avg' across a list of dictionaries.
    
    Args:
        data (List[Dict]): List of dictionaries with metrics
        
    Returns:
        Dict[str, float]: Dictionary with average values for 'avg*' keys
    """
    if not data:
        return {}

    totals = {}
    count = len(data)

    for entry in data:
        for key, value in entry.items():
            if key.startswith('avg') and isinstance(value, (int, float)):
                totals[key] = totals.get(key, 0.0) + value

    return {key: total / count for key, total in totals.items()}

def results_to_dataframe(results: List[Dict], m: int = None, ef_construct: int = None) -> pd.DataFrame:
    """
    Convert results to a pandas DataFrame.
    
    Args:
        results (List[Dict]): List of result dictionaries
        m (int): HNSW M parameter
        ef_construct (int): HNSW ef_construct parameter
        
    Returns:
        pd.DataFrame: DataFrame with results
    """
    df = pd.DataFrame(results)
    
    if m is not None:
        df['m'] = m
    
    if ef_construct is not None:
        df['ef_construct'] = ef_construct
    
    # Round floating point numbers for better readability
    if 'avg_precision' in df.columns:
        df['avg_precision'] = df['avg_precision'].round(6)
    
    if 'avg_query_time_ms' in df.columns:
        df['avg_query_time_ms'] = df['avg_query_time_ms'].round(6)
    
    return df