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
    prompt = f"""
    INPUT:

    Role: You are an expert in generating interview questions for academic positions with a strong understanding of the client's vision.

    Context: The user's requirements for the question you are analyzed. You have a solid understanding of their needs.

    Level: Based on the chosen level, provide questions to help the user improve their skills.

    Please generate {queries_num} interview questions for the topic "{topic_title}" suitable for an {level} level interview.

    Topic Chosen: {topic_title}
    Number of Questions: {queries_num}
    """

    request_body = {
        "prompt": {
            "text": prompt
        }
    }

    try:
        response = requests.post(f"{endpoint}/models/text-bison-001:generateText?key={api_key}", json=request_body)
        response.raise_for_status()
        data = response.json()
        questions = data.get('candidates', [])[0].get('output', '').strip().split('\n')
        return questions
    except requests.exceptions.RequestException as e:
        return [f"An error occurred: {e}"]
    except KeyError:
        return ["Unexpected response format from the API."]

def get_ai_feedback(question, answer):
    prompt = f"""
    Provide feedback on the candidate's response. Please take the "{question}" as the question which is being answered by the interview candidate. 
    And take "{answer}" as the answer for the "{question}" which is asked in the interview. If user entered more that one question, the feedback should be overall of the questions.

    Additionally, focus on:
        - Provide feedback on how they can improve to impress the interviewer - Max of 5 lines ONLY
        - How to improve their response - Max of 3 lines ONLY
        - Where the candidate gave a good answer - Max of 3 lines ONLY
        - Where they went wrong - Max of 5 lines ONLY
        - Suggestions for improvement (must) - Max of 3 lines ONLY
        - Additional tips - Max of 5 points ONLY
        - Assign a score out of 100 ONLY based on the overall quality of the response, considering the above criteria - Max of 2 lines ONLY
    
    NOTE : 
        - DO NOT REPEAT THE QUESTION IN THE FEEDBACK AND ALSO THE FEEDBACK SHOULD BE IN BULLET POINTS.
        - DO NOT INCLUDE ANY PROMPTS OR EXPLANATIONS IN THE FEEDBACK.
        - DO NOT REPEAT TEXT OR ANY WORD, SHOULD BE UNIQEUE.

    Your role after the feedback generation is to Format the feedback as follows:
     - Make usre you use new lines to maintain the proper alienment.
     - Write a brief summary of your overall impression of the answer.
    Areas for Improvement:
       - Identify one area where the answer could be improved. Use **bold text** for the key point.
       - Suggest user area for improvement.
       - Mention any other improvements that could be made.
    Highlights:
       - Highlight a particular aspect of the answer that stood out. Use **yellow text** for emphasis and explain why it was impressive.
    """

    request_body = {
        "prompt": {
            "text": prompt
        }
    }

    try:
        response = requests.post(f"{endpoint}/models/text-bison-001:generateText?key={api_key}", json=request_body)
        response.raise_for_status()
        data = response.json()
        feedback = data.get('candidates', [])[0].get('output', '').strip()
        return feedback
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except KeyError:
        return "Unexpected response format from the API."

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        topic_title = request.form['topic_title']
        queries_num = int(request.form['queries_num'])
        questions = generate_questions(topic_title, queries_num)
        return render_template('index.html', questions=questions, topic_title=topic_title, queries_num=queries_num)
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    questions = request.form.getlist('questions')
    answers = request.form.getlist('answers')
    feedbacks = [get_ai_feedback(question, answer) for question, answer in zip(questions, answers)]
    return render_template('index.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
