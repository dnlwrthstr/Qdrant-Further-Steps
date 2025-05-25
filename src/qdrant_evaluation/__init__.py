"""
Qdrant Evaluation Package

This package provides tools for evaluating and benchmarking 
different configurations of the Qdrant vector database.
"""

from .client import get_client, load_environment, update_collection_config
from .embedding import get_embedding, load_test_dataset
from .evaluator import (
    precision_k,
    get_ann_points,
    get_hnsw_points,
    get_knn_points,
    get_ann_points_quantized,
    get_knn_points_ignoring_quantization,
    evaluate_ann,
    evaluate_hnsw_ef,
    evaluate_ann_quantized,
    compute_avg_metrics,
    results_to_dataframe
)

__all__ = [
    'get_client',
    'load_environment',
    'update_collection_config',
    'get_embedding',
    'load_test_dataset',
    'precision_k',
    'get_ann_points',
    'get_hnsw_points',
    'get_knn_points',
    'get_ann_points_quantized',
    'get_knn_points_ignoring_quantization',
    'evaluate_ann',
    'evaluate_hnsw_ef',
    'evaluate_ann_quantized',
    'compute_avg_metrics',
    'results_to_dataframe'
]