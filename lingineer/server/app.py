from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import speech_recognition as sr
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('API_KEY')
endpoint = "https://generativelanguage.googleapis.com/v1beta"

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/chat', methods=['POST'])
def chat_with_coach():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid input, expected JSON"}), 400

        data = request.json
        scenario = data.get("scenario")
        user_message = data.get("message")

        if not scenario or not user_message:
            return jsonify({"error": "Missing 'scenario' or 'message'"}), 400

        prompt = f"You are an AI coach helping users with English in engineering contexts. Scenario: {scenario}. User said: '{user_message}'. Provide constructive feedback, correct any mistakes, and give suggestions to improve."

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

        response = requests.post(
            f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
            json=request_body
        )

        if response.status_code == 200:
            result = response.json()
            feedback = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if feedback:
                formatted_feedback = feedback.replace('. ', '.<br/><br>').replace('\n', '<br/>')
                return jsonify({"feedback": formatted_feedback})
            else:
                return jsonify({"error": "No feedback received from the AI"}), 500
        else:
            return jsonify({"error": "Failed to retrieve response from AI"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pronunciation', methods=['POST'])
def pronunciation_practice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']
    audio_path = "/tmp/user_recording.wav"
    audio_file.save(audio_path)

    audio = AudioSegment.from_file(audio_path)
    audio.export(audio_path, format="wav")

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data)
            
            sample_text = "I am practicing my pronunciation"
            feedback = compare_pronunciation(user_text, sample_text)
            
            return jsonify({"feedback": feedback})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError:
        return jsonify({"error": "Error with speech recognition service"}), 500

def compare_pronunciation(user_text, sample_text):
    if user_text.lower() == sample_text.lower():
        return "Excellent pronunciation!"
    else:
        return f"Your pronunciation differed. You said: '{user_text}'"

if __name__ == '__main__':
    port = 5001
    app.run(debug=True, port=port)
