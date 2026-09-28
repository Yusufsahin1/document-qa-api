from sentence_transformers import SentenceTransformer

# Load the model once globally when the module is imported (Singleton behavior)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates vector embeddings for a list of text strings (e.g., document chunks).

    Args:
        texts (list[str]): List of texts to be embedded.

    Returns:
        list[list[float]]: List of 384-dimensional float vectors.
    """
    embeddings = model.encode(texts)
    embeddings_list = embeddings.tolist()
    return embeddings_list


def generate_query_embedding(text: str) -> list[float]:
    """
    Generates a single vector embedding for a query string (e.g., user question).

    Args:
        text (str): Query text.

    Returns:
        list[float]: A 384-dimensional float vector.
    """
    return generate_embeddings([text])[0]
    