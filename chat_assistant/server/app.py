from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load API key from environment variables
load_dotenv(find_dotenv()) 
api_key = os.getenv('GOOGLE_API_KEY')

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_query = request.json['user_query']

    # Set the prompt for healthcare conversation
    prompt = f"Healthcare conversation:\nUser: {user_query}\nHealthcare AI:"

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

    # Parse the response
    response_json = response.json()

    # Get the generated content from the response
    generated_content = response_json["candidates"][0]['content']['parts'][0]['text']

    return jsonify({"healthcare_response": generated_content})

if __name__ == '__main__':
    app.run(debug=True)


    
    