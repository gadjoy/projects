from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv, find_dotenv
from werkzeug.utils import secure_filename
import docx
import PyPDF2
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv(find_dotenv())
api_key = os.getenv('YOUR_API_KEY')  # Ensure you set this in your .env file

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Directory where the uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from DOCX files
def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

# Function to extract text from PDF files
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/')
def index():
    return 'Welcome to the Resume Customization Tool!'

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from the resume
        if filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        elif filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)

        return jsonify({"message": "Resume uploaded successfully", "resume_text": resume_text}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/generate_customized_resume', methods=['POST'])
def generate_customized_resume():
    logging.debug("Received request to generate customized resume")
    try:
        resume_text = request.json.get('resume_text')
        job_description = request.json.get('job_description')

        if not resume_text or not job_description:
            return jsonify({"error": "Both resume text and job description are required"}), 400

        # Set the prompt for the API
        prompt = f"Customize the following resume based on this job description:\n\nJob Description: {job_description}\n\nResume: {resume_text}\n\nCustomized Resume:"

        # Set the API endpoint
        endpoint = "https://generativelanguage.googleapis.com/v1beta"

        # Prepare the request body
        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Make the request to the API
        response = requests.post(
            f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
            json=request_body,
        )

        # Check if the response is successful
        if response.status_code != 200:
            logging.error(f"Failed to generate response from the API, status code: {response.status_code}, message: {response.text}")
            return jsonify({"error": f"Failed to generate response from the API"}), 500

        # Parse the response
        response_json = response.json()

        # Check if the response contains expected data
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            customized_resume = response_json["candidates"][0]['content']['parts'][0]['text']
            return jsonify({"customized_resume": customized_resume}), 200
        else:
            return jsonify({"error": "No valid response from the API"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
