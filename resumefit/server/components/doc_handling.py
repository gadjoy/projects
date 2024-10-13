import markdown
import pdfkit
from docx import Document

def markdown_to_doc(markdown_text, pdf_path, doc_path):
    """
    Convert markdown to PDF
    """
    html = markdown.markdown(markdown_text)
    pdfkit.from_string(html, pdf_path)

    doc = Document()
    doc.add_paragraph(markdown_text)
    doc.save(doc_path)