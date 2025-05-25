# Test script to verify that both packages can be imported correctly
try:
    # Import from qdrant_evaluation
    from qdrant_evaluation.client import get_client
    from qdrant_evaluation.evaluator import evaluate_ann
    print("Successfully imported from qdrant_evaluation package")
    
    # Import from qdrant_data_ingestion
    from qdrant_data_ingestion import DataIngestion, ingest_from_file
    print("Successfully imported from qdrant_data_ingestion package")
    
    print("All imports successful! Both packages are correctly installed.")
except ImportError as e:
    print(f"Import error: {e}")
    print("One or both packages are not correctly installed.")