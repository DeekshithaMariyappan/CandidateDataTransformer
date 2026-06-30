import pdfplumber

class PDFExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text(self) -> str:
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text
