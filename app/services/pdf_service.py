import fitz  # PyMuPDF


def extract_text(path: str) -> str:
    """
    Extract text from a PDF file.
    Returns combined text from all pages.
    """

    try:
        extracted_text = []

        with fitz.open(path) as doc:

            for page_number, page in enumerate(doc, start=1):

                page_text = page.get_text("text")

                if page_text:
                    page_text = page_text.strip()

                    if page_text:
                        extracted_text.append(f"--- Page {page_number} ---")
                        extracted_text.append(page_text)

        return "\n".join(extracted_text)

    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")