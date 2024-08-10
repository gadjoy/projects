import PyPDF2
from transformers import pipeline


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_response(pdf_text, user_message):
    # Initialize the QA pipeline
    qa_pipeline = pipeline("question-answering")
    response = qa_pipeline(question=user_message, context=pdf_text)
    return response['answer']
