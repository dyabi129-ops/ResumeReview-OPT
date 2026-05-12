"""
PDF Reader Utility
Extracts text from an uploaded PDF resume.
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Takes a Streamlit uploaded file object and extracts all text from it.
    Returns a single string with the full resume text.
    """
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()
    return full_text.strip()
