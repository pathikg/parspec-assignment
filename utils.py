import pymupdf as pdf


def extract_text(pdf_path):
    try:
        # Extract text using PyMuPDF
        doc = pdf.open(pdf_path)
        text = ""
        first_page_text = doc[0].get_text()
        for page in doc:
            text += page.get_text()

        # Extract label from filename
        return text, first_page_text
    except Exception as e:
        print(f"Error extracting text from PDF")
        return None
