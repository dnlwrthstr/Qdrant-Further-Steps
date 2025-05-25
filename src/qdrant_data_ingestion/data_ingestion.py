"""
Qdrant Data Ingestion Module

This module provides functionality to ingest data into a Qdrant vector database.
It handles streaming data from JSON files, creating collections, and uploading vectors with payloads.
"""

import json
import logging
import os
import uuid
from typing import Any, Dict, Generator, List, Optional, Union

from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, PointStruct, VectorParams
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def stream_json(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """
    Stream JSON objects from a file, one object per line.

    Args:
        file_path: Path to the JSON file

    Yields:
        Dict[str, Any]: JSON objects from the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If a line contains invalid JSON
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON at line {line_num}: {e}")
                    raise
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise


class DataIngestion:
    """
    A class for ingesting data into Qdrant vector database.

    This class handles the process of connecting to a Qdrant server,
    creating collections if they don't exist, and uploading vectors with payloads.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        grpc_port: int = 6334,
        prefer_grpc: bool = True,
        api_key: Optional[str] = None,
        timeout: int = 120,
        batch_size: int = 1000
    ):
        """
        Initialize the DataIngestion instance.

        Args:
            host: Qdrant server host
            port: Qdrant server HTTP port
            grpc_port: Qdrant server gRPC port
            prefer_grpc: Whether to prefer gRPC over HTTP
            api_key: API key for authentication
            timeout: Request timeout in seconds
            batch_size: Number of points to upload in a single batch
        """
        self.client = QdrantClient(
            host=host,
            port=port,
            grpc_port=grpc_port,
            prefer_grpc=prefer_grpc,
            api_key=api_key,
            timeout=timeout
        )
        self.batch_size = batch_size
        logger.info(f"Initialized DataIngestion with batch size {batch_size}")

    def create_collection_if_not_exists(
        self,
        collection_name: str,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE,
        hnsw_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Create a collection if it doesn't exist.

        Args:
            collection_name: Name of the collection
            vector_size: Size of the vectors
            distance: Distance metric to use
            hnsw_config: HNSW index configuration
        """
        vectors_config = VectorParams(
            size=vector_size,
            distance=distance
        )

        if not self.client.collection_exists(collection_name=collection_name):
            logger.info(f"Creating collection: {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config
            )

            if hnsw_config:
                logger.info(f"Updating collection with HNSW config: {hnsw_config}")
                self.client.update_collection(
                    collection_name=collection_name,
                    hnsw_config=models.HnswConfigDiff(**hnsw_config)
                )
        else:
            logger.info(f"Collection {collection_name} already exists")

    def prepare_payload(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare payload from a record.

        Args:
            record: Record containing data for the payload

        Returns:
            Dict[str, Any]: Prepared payload
        """
        return {
            "id": record.get("id"),
            "submitter": record.get("submitter"),
            "title": record.get("title"),
            "abstract": record.get("abstract"),
            "authors": record.get("authors"),
            "categories": record.get("categories"),
            "comments": record.get("comments"),
            "license": record.get("license"),
            "versions": record.get("versions"),
            "doi": record.get("doi"),
            "update_date": record.get("update_date"),
            "journal-ref": record.get("journal-ref"),
            "report-no": record.get("report-no"),
            "authors_parsed": record.get("authors_parsed")
        }

    def create_point(self, record: Dict[str, Any]) -> Optional[PointStruct]:
        """
        Create a point from a record.

        Args:
            record: Record containing data for the point

        Returns:
            Optional[PointStruct]: Created point or None if embedding is missing
        """
        embedding = record.get("embedding")
        if embedding is None:
            logger.warning(f"Skipping record without embedding: {record.get('id')}")
            return None

        payload = self.prepare_payload(record)

        return PointStruct(
            id=str(uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=record["id"])),
            vector=embedding,
            payload=payload,
        )

    def ingest_data(
        self,
        file_path: str,
        collection_name: str,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE,
        hnsw_config: Optional[Dict[str, Any]] = None,
        show_progress: bool = True
    ) -> int:
        """
        Ingest data from a file into a collection.

        Args:
            file_path: Path to the JSON file
            collection_name: Name of the collection
            vector_size: Size of the vectors
            distance: Distance metric to use
            hnsw_config: HNSW index configuration
            show_progress: Whether to show progress bar

        Returns:
            int: Number of points ingested
        """
        # Ensure the collection exists
        self.create_collection_if_not_exists(
            collection_name=collection_name,
            vector_size=vector_size,
            distance=distance,
            hnsw_config=hnsw_config
        )

        # Stream data from file
        generator = stream_json(file_path)
        batch: List[PointStruct] = []
        total_ingested = 0

        # Wrap with tqdm if progress should be shown
        if show_progress:
            generator = tqdm(generator, desc=f"Uploading points to {collection_name}")

        for record in generator:
            point = self.create_point(record)
            if point is None:
                continue

            batch.append(point)

            if len(batch) >= self.batch_size:
                self.client.upsert(collection_name=collection_name, points=batch)
                total_ingested += len(batch)
                batch.clear()

        # Upload remaining points
        if batch:
            self.client.upsert(collection_name=collection_name, points=batch)
            total_ingested += len(batch)

        logger.info(f"Ingested {total_ingested} points into collection {collection_name}")
        return total_ingested


def ingest_from_file(
    file_path: str,
    collection_name: str,
    host: str = "localhost",
    port: int = 6333,
    grpc_port: int = 6334,
    batch_size: int = 1000,
    vector_size: int = 1536,
    distance: Union[Distance, str] = Distance.COSINE,
    show_progress: bool = True
) -> int:
    """
    Convenience function to ingest data from a file into a collection.

    Args:
        file_path: Path to the JSON file
        collection_name: Name of the collection
        host: Qdrant server host
        port: Qdrant server HTTP port
        grpc_port: Qdrant server gRPC port
        batch_size: Number of points to upload in a single batch
        vector_size: Size of the vectors
        distance: Distance metric to use
        show_progress: Whether to show progress bar

    Returns:
        int: Number of points ingested
    """
    # Convert string distance to enum if needed
    if isinstance(distance, str):
        distance = Distance[distance.upper()]

    ingestion = DataIngestion(
        host=host,
        port=port,
        grpc_port=grpc_port,
        batch_size=batch_size
    )

    return ingestion.ingest_data(
        file_path=file_path,
        collection_name=collection_name,
        vector_size=vector_size,
        distance=distance,
        show_progress=show_progress
    )
