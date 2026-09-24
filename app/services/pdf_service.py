import pymupdf  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF file and returns it as a list of dictionaries.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list[dict]: A list of dictionaries containing the extracted text and page information.
    """
    doc = pymupdf.open(file_path)
    text_data = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_data.append({"page": page_num + 1, "text": text})

    doc.close()
    return text_data