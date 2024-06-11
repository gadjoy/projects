import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from environment variable
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

# Define the API endpoint
endpoint = "https://generativelanguage.googleapis.com/v1beta2"

def generate_questions(topic_title, queries_num, level="Easy"):
    # Derive field name from the topic title (for demonstration purposes, we use the topic title directly)
    field_name = topic_title

    # Create a well-structured and professional prompt
    prompt = f"""
    Role: You are an expert in generating interview questions for academic positions with a strong understanding of the client's vision.

    Context: The client's requirements for a software project are analyzed. You have a solid understanding of their needs.

    Level: Based on the chosen level, provide questions to help the user improve their skills.

    Explore: When refining the prompt, ensure that the field name provided is both specific and relevant to the content of the query.
    Consider the broader category as well as any subfields that might better capture the essence of the user's request.
    This will help in providing a clear and concise field name that accurately reflects the user's needs, and store it in new variable.

    Field Name: {field_name}

    Topic Chosen: {topic_title}
    Number of Questions: {queries_num}

    Please generate {queries_num} interview questions for the topic "{topic_title}" suitable for an easy level interview.
    """

    # Prepare the request body
    request_body = {
        "prompt": {
            "text": prompt
        }
    }

    # Function to get questions from the API
    try:
        response = requests.post(f"{endpoint}/models/text-bison-001:generateText?key={api_key}", json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        questions = data.get('candidates', [])[0].get('output', '').strip().split('\n')
        return questions
    except requests.exceptions.RequestException as e:
        return [f"An error occurred: {e}"]
    except KeyError:
        return ["Unexpected response format from the API."]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic_title = request.form['topic_title']
        queries_num = int(request.form['queries_num'])
        questions = generate_questions(topic_title, queries_num)
        return render_template('index.html', questions=questions, topic_title=topic_title, queries_num=queries_num)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
