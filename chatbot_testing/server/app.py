from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

_ = load_dotenv(find_dotenv())  # read local .env file
api_key = os.environ['GOOGLE_API_KEY']

endpoint = "https://generativelanguage.googleapis.com/v1beta"

@app.route('/generate', methods=['POST'])
def generate_content():
    chat_conversation = request.json.get('text')  # Get prompt from POST data

    prompt = f" This is a chat conversation between a user and a chatbot. Design test scenarios and list comprehensive test cases for such a converstaion to identify errors and evaluate response. Please use the relevant chatbot testing guidelines. Please give the output in a properly formatted markdown The conversation is given here {chat_conversation}"

    if not prompt:
        return jsonify({'error': 'Please provide a prompt'}), 400

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
        json=request_body,
    )

    if response.status_code == 200:
        response_json = response.json()
        generated_content = response_json["candidates"][0]['content']['parts'][0]['text']
        return jsonify({'content': generated_content})
    else:
        return jsonify({'error': 'Content generation failed'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True) 
