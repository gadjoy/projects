from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from flask_cors import CORS
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app)

# Initialize OpenAI client
openai.api_key = os.environ.get('OPENAI_API_KEY')


@app.route('/generate_question', methods=['GET'])
def generate_question():
    prompt = "Generate a general interview question:"

    endpoint = "https://generativelanguage.googleapis.com/v1beta"
    api_key = os.environ.get('GOOGLE_API_KEY')
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
            f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
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

    try:
        # Create a secure filename
        filename = secure_filename(file.filename)
        # Create a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(temp_path)
        
        with open(temp_path, 'rb') as audio_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return jsonify({"transcription": transcription['text']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcribe_blob', methods=['POST'])
def transcribe_audio_blob():
    audio_file = request.files.get('audio')
    if audio_file:
        filename = secure_filename(audio_file.filename)
        filename = os.path.splitext(filename)[0] + ".mp3"  # Change the extension to .mp3
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        audio_file.save(temp_path)

        with open(temp_path, 'rb') as audio_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return jsonify({"transcription": transcription['text']}), 200
    else:
        return jsonify({"error": "No file received"}), 400

@app.route('/generate_feedback', methods=['POST'])
def generate_feedback():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"This is a recording of a candidate preparing for interview, please provide feedback on how they can improve to impress the interviewer.\n{data['text']}"

    endpoint = "https://generativelanguage.googleapis.com/v1beta"
    api_key = os.environ.get('GOOGLE_API_KEY')
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
            f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
            json=request_body
        )
        response_json = response.json()
        generated_content = response_json["candidates"][0]['content']['parts'][0]['text']
        return jsonify({"generated_content": generated_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
