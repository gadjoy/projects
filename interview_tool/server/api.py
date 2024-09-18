import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Google API key
api_key = os.environ.get('GOOGLE_API_KEY')

@app.route('/generate_question', methods=['GET'])
def generate_question():
    prompt = "Generate a general interview question:"
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
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

    try:
        response = requests.post(
            f"{endpoint}?key={api_key}",
            json=request_body
        )
        response_json = response.json()
        generated_question = response_json["candidates"][0]['content']['parts'][0]['text']
        return jsonify({"generated_question": generated_question}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(temp_path)
    
    try:
        # Assuming the Google API provides a similar service
        response = requests.post(
            f"https://your-transcription-api-endpoint?key={api_key}",
            files={"file": open(temp_path, 'rb')}
        )
        response_json = response.json()
        transcription = response_json.get("transcription", "No transcription available")
        
        os.remove(temp_path)
        return jsonify({"transcription": transcription}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_feedback', methods=['POST'])
def generate_feedback():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"This is a recording of a candidate preparing for interview, please provide feedback on how they can improve to impress the interviewer.\n{data['text']}"

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
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

    try:
        response = requests.post(
            f"{endpoint}?key={api_key}",
            json=request_body
        )
        response_json = response.json()
        generated_content = response_json["candidates"][0]['content']['parts'][0]['text']
        return jsonify({"generated_content": generated_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
