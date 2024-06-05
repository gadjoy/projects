from flask import Flask, request, jsonify
from openai import OpenAI
import os
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI()

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Convert the FileStorage to a BytesIO object
        file_stream = BytesIO(file.read())
        file_stream.seek(0)  # Important to rewind after reading for the API call
        
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file_stream
        )
        return jsonify({"transcription": transcription.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_content', methods=['POST'])
def generate_content():
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


# Path: server/test_api.py
import requests
from flask import request

