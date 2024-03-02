from flask import Flask, request, jsonify
import requests
import os, json
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set the API key
api_key = os.environ['GOOGLE_API_KEY']

# Set the API endpoint
endpoint = "https://generativelanguage.googleapis.com/v1beta"

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/generate', methods=['POST'])
def generate_questions():
    # try:
        # Get data from the request
    data = request.json

    num_questions = data["num_questions"]
    topic = data["topic"]
    difficulty = data["difficulty"].upper()  # Ensure uppercase for consistency

    # num_questions = 2
    # topic = "Python"
    # difficulty = "EASY"

    prompt = f"Give me {num_questions} multiple choice questions about {topic}. The questions should be at a {difficulty} level. Return your answer entirely in the form of a JSON object. The JSON object should have a key named 'questions' which is an array of the questions. Each quiz question should include the choices, the answer, and a brief explanation of why the answer is correct. Don't include anything other than the JSON. The JSON properties of each question should be 'query' (which is the question), 'choices', 'answer', and 'explanation'. The choices shouldn't have any ordinal value like A, B, C, D or a number like 1, 2, 3, 4. The answer should be the 0-indexed number of the correct choice."

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

    # Make the request to Generative Language API
    response = requests.post(
        f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
        json=request_body,
    )

    # Check if 'questions' key exists in the response JSON
    if response.status_code == 200:
        # response_json = response.json()
        questions = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'].replace("```json",'').replace("```",'').strip())['questions']
        return jsonify({"questions": questions}), 200
    else:
        return jsonify({'error': 'Content generation failed'}), response.status_code
    
@app.route('/mock_generate', methods=['POST'])
def mock_generate_questions():
    data = request.json

    num_questions = data["num_questions"]
    topic = data["topic"]
    difficulty = data["difficulty"].upper()

#     mock_questions = [
#     {
#       "answer": 3,
#       "choices": [
#         "integer",
#         "string",
#         "boolean",
#         "all of the above"
#       ],
#       "explanation": "Python has three built-in data types: integer, string, and boolean.",
#       "query": "Which of the following is a valid data type in Python?"
#     },
#     {
#       "answer": 2,
#       "choices": [
#         "5",
#         "10",
#         "15",
#         "105"
#       ],
#       "explanation": "The '+' operator is used for addition in Python. So, the expression '10 + 5' evaluates to 15.",
#       "query": "What is the output of the following Python code?\n\npython\nprint(10 + 5)\n"
#     }
#   ]
    
    mock_questions = [
    {
        "answer": 0,
        "choices": [
        "integer",
        "string",
        "boolean"
        ],
        "explanation": "All three choices are valid data types in Python.",
        "query": "Which of the following is a valid data type in Python?"
    },
    {
        "answer": 0,
        "choices": [
        "variable_name = value",
        "creating_a_variable value",
        "value = variable_name"
        ],
        "explanation": "In Python, you assign a value to a variable using the '=' operator.",
        "query": "How do you create a variable in Python?"
    }
    ]

    return jsonify({"questions": mock_questions}), 200


if __name__ == '__main__':
    app.run(debug=True)
