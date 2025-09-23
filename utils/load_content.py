def load_content(file_path):
    """Load text or PDF content from disk.

    This function delays importing heavy PDF parsing libraries until a
    PDF is actually requested, so the module can be imported in
    environments where those optional deps aren't installed.
    """
    if file_path.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except Exception:
            raise ModuleNotFoundError(
                "pypdf is required to read PDF files. Install with:\n"
                "    pip install pypdf"
            )

        pdf = PdfReader(file_path)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        print("Unsupported file format")
        return ""


def load_content_streamlit(upload_file):
    """Load content from an uploaded file object in Streamlit.

    We import PyPDF2 lazily to avoid import-time failures when the
    dependency is missing.
    """
    if upload_file is not None:
        try:
            import PyPDF2
        except Exception:
            raise ModuleNotFoundError(
                "PyPDF2 is required for streamlit PDF parsing. Install with:\n"
                "    pip install PyPDF2"
            )

        pdf_reader = PyPDF2.PdfReader(upload_file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() or ""
        return content
