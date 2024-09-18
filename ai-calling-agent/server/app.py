from flask import Flask, render_template, request, jsonify, send_from_directory
from call_handler import make_call
import os
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../client', static_folder='../client')
UPLOAD_FOLDER = 'server/uploaded_scripts'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/make_call', methods=['POST'])
def handle_make_call():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    
    # Handle file upload
    if 'script_file' in request.files:
        script_file = request.files['script_file']
        if script_file.filename != '':
            script_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(script_file.filename))
            script_file.save(script_path)
            # Read the script content
            try:
                with open(script_path, 'r') as file:
                    script_content = file.read()
                result = make_call(name, phone_number, script_content)
            except Exception as e:
                logging.error(f"Error reading script file or making call: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        else:
            return jsonify({'error': 'No script file provided'}), 400
    else:
        return jsonify({'error': 'Script file is required'}), 400

    # Debugging output
    logging.debug(f"Result: {result}")

    # Check if result is JSON-serializable and has a 'completed' key
    if isinstance(result, dict) and 'completed' in result:
        return jsonify({'message': result}), 200
    elif isinstance(result, str):
        return jsonify({'message': result}), 200
    else:
        return jsonify({'error': 'Unexpected result format'}), 500

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    transcript_path = "server/latest_transcription.json"
    if os.path.exists(transcript_path):
        try:
            with open(transcript_path, "r") as file:
                transcript = json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from transcript file: {e}")
            transcript = []
    else:
        transcript = []
    return jsonify(transcript)

@app.route('/get_call_logs', methods=['GET'])
def get_call_logs():
    call_logs_path = "server/call_logs.json"
    if os.path.exists(call_logs_path):
        try:
            with open(call_logs_path, "r") as file:
                call_logs = json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from call logs file: {e}")
            call_logs = []
    else:
        call_logs = []
    return jsonify(call_logs)

if __name__ == '__main__':
    app.run(debug=True)
