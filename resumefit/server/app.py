from flask import Flask, request, jsonify, send_file
from components.llm_process import process_resume_with_openai
from components.cleanup import clean_string, extract_message_content
from flask_cors import CORS
import os
import pypandoc

app = Flask(__name__)
CORS(app)

API_VERSION = "0.0.3"
RELEASE_NOTES = "limit characters, add download endpoint, versioning, cookie tracking, release notes "
RELEASE_DATE = "2022-10-12"

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Resume Customizer API",
        "api_version": API_VERSION,
        "release_notes": RELEASE_NOTES,
        "release_date": RELEASE_DATE
    }), 200

@app.route('/version')
def version():
    return jsonify({"version": API_VERSION, "release_date": RELEASE_DATE, "release_notes": RELEASE_NOTES}), 200

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
    response.headers['X-API-Version'] = API_VERSION
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
    
    pypandoc.convert_text(
        processed_resume, 
        'pdf', 
        format='md', 
        outputfile='processed_resume.pdf', 
        extra_args=['-V', 'geometry:margin=1in'])
    pypandoc.convert_text(
        processed_resume, 
        'docx', 
        format='md', 
        outputfile='processed_resume.docx',
        extra_args=['--reference-doc=reference.docx']
        )

    response = jsonify({
        "customized_resume": processed_resume
        })
    response.headers['X-API-Version'] = API_VERSION
    return response, 200

@app.route('/download/<file_type>', methods=['GET'])
def download_file(file_type):
    if file_type == 'pdf':
        file_path = 'processed_resume.pdf'
    elif file_type == 'doc':
        file_path = 'processed_resume.docx'
    else:
        return jsonify({"error": "Invalid file type"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use PORT environment variable or default to 8080
    app.run(host='0.0.0.0', port=port, debug=True)