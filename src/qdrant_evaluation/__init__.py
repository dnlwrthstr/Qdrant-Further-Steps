"""
Qdrant Evaluation Package

This package provides tools for evaluating and benchmarking 
different configurations of the Qdrant vector database.
"""

from .client import get_client, load_environment, update_collection_config
from .embedding import get_embedding, load_test_dataset
from .collection import wait_for_collection_green
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
    evaluate_with_quantization,
    compute_avg_metrics,
    results_to_dataframe,
    evaluate_collection_with_config
)

__all__ = [
    'get_client',
    'load_environment',
    'update_collection_config',
    'get_embedding',
    'load_test_dataset',
    'wait_for_collection_green',
    'precision_k',
    'get_ann_points',
    'get_hnsw_points',
    'get_knn_points',
    'get_ann_points_quantized',
    'get_knn_points_ignoring_quantization',
    'evaluate_ann',
    'evaluate_hnsw_ef',
    'evaluate_ann_quantized',
    'evaluate_with_quantization',
    'compute_avg_metrics',
    'results_to_dataframe',
    'evaluate_collection_with_config'
]
