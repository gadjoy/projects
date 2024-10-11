from flask import Flask, request, jsonify
from components.llm_process import process_resume_with_openai
from components.cleanup import clean_string, extract_message_content
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

APP_VERSION = "0.0.1"
RELEASE_NOTES = "Initial release with basic functionality with docker & gcloud"
RELEASE_DATE = "2022-10-10"

@app.route('/')
def home():
    return jsonify({
        "app_version": APP_VERSION,
        "release_notes": RELEASE_NOTES,
        "release_date": RELEASE_DATE
    }), 200

@app.route('/input', methods=['POST'])
def input_resume():
    data = request.json
    base_resume = data.get('base_resume')
    job_description = data.get('job_description')
    
    if not base_resume or not job_description:
        return jsonify({"error": "base_resume and job_description are required"}), 400
    
    # Process the resume with Google API
    message = process_resume_with_openai(base_resume, job_description)

    raw_markdown = extract_message_content(message)

    # Clean the raw markdown
    processed_resume = clean_string(raw_markdown)

    with open('processed_resume.txt', 'w') as file:
        file.write(processed_resume)
    
    response = jsonify({"message": "Resume processed successfully"})
    response.headers['X-API-Version'] = APP_VERSION
    return response, 200

@app.route('/output', methods=['GET'])
def output_resume():
    if not os.path.exists('processed_resume.txt'):
        return jsonify({"error": "No resume processed yet"}), 400

    try:
        with open('processed_resume.txt', 'r') as file:
            processed_resume = file.read()
    except IOError:
        return jsonify({"error": "Error reading the processed resume file"}), 500

    response = jsonify({"customized_resume": processed_resume})
    response.headers['X-API-Version'] = APP_VERSION
    return response, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use PORT environment variable or default to 8080
    app.run(host='0.0.0.0', port=port, debug=True)