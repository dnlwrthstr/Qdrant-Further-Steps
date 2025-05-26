from qdrant_client import QdrantClient
import time
from typing import Optional


def wait_for_collection_green(client: QdrantClient, collection_name: str, timeout: int = 600) -> None:
    """
    Waits until the collection status is 'Green' or until timeout.

    Args:
        client: Qdrant client
        collection_name: Name of the collection
        timeout: Maximum wait time in seconds (default: 600 seconds / 10 minutes)
    """
    start_time = time.time()

    while True:
        status = client.get_collection(collection_name).status
        if status == "green":
            print(f"Collection {collection_name} is ready.")
            break

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Collection {collection_name} did not become ready in {timeout} seconds.")

        time.sleep(0.5)  # Poll every 500ms
