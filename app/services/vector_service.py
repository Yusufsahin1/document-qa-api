import faiss
import numpy as np


def create_index(dimension: int = 384) -> faiss.IndexFlatL2:
    """
    Creates a new empty FAISS index using L2 (Euclidean) distance.

    Args:
        dimension (int): Dimension of the embedding vectors. Defaults to 384.

    Returns:
        faiss.IndexFlatL2: An empty FAISS index instance.
    """
    return faiss.IndexFlatL2(dimension)


def add_vectors(index: faiss.IndexFlatL2, vectors: list[list[float]]) -> None:
    """
    Converts Python list vectors into a float32 NumPy array and adds them to the FAISS index.

    Args:
        index (faiss.IndexFlatL2): The FAISS index to store vectors.
        vectors (list[list[float]]): List of embedding vectors.
    """
    vectors_np = np.array(vectors, dtype=np.float32)
    index.add(vectors_np)


def search_vectors(index: faiss.IndexFlatL2, query_vector: list[float], top_k: int = 3) -> tuple[list[float], list[int]]:
    """
    Searches the FAISS index for the top_k nearest vector neighbors to the given query vector.

    Args:
        index (faiss.IndexFlatL2): The populated FAISS index.
        query_vector (list[float]): The single 384-dimensional query vector.
        top_k (int): Number of most similar results to return. Defaults to 3.

    Returns:
        tuple[list[float], list[int]]: A tuple containing (distances, indices).
            - distances: L2 distance values for top_k results.
            - indices: Integer indices corresponding to stored vectors/metadata.
    """
    query_np = np.array([query_vector], dtype=np.float32)
    distances, indices = index.search(query_np, top_k)
    return distances[0].tolist(), indices[0].tolist()


def save_index(index: faiss.IndexFlatL2, file_path: str) -> None:
    """
    Saves the FAISS index to a file on disk.

    Args:
        index (faiss.IndexFlatL2): The FAISS index to persist.
        file_path (str): Destination file path (e.g. app/storage/faiss_index/index.faiss).
    """
    faiss.write_index(index, file_path)


def load_index(file_path: str) -> faiss.IndexFlatL2:
    """
    Loads a FAISS index from a file on disk.

    Args:
        file_path (str): Path to the saved FAISS index file.

    Returns:
        faiss.IndexFlatL2: Loaded FAISS index instance.
    """
    return faiss.read_index(file_path)