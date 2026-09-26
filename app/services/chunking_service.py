def chunk_pages(pages: list[dict], document_id: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:

    """
    Splits text from extracted PDF pages into smaller overlapping chunks 
    and attaches relevant metadata to each chunk.

    Args:
        pages (list[dict]): A list of dictionaries containing 'page' and 'text'.
        document_id (str): Unique identifier or filename of the document.
        chunk_size (int): Maximum character length of each chunk. Defaults to 500.
        overlap (int): Number of overlapping characters between consecutive chunks. Defaults to 50.

    Returns:
        list[dict]: A list of chunk dictionaries containing text and metadata.
    """

    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"].strip()
        page_num = page["page"]

        if not text:
            continue

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({
                "chunk_id": chunk_index,
                "text": chunk,
                "document_id": document_id,
                "page": page_num,
                "chunk_index": chunk_index
            })
            chunk_index += 1
            start = end - overlap # start += chunk_size - overlap

    return chunks