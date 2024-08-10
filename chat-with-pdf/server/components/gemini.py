import requests

API_KEY = 'AIzaSyCRpCK-u1LhR_IfXPf3XSw8Qb7UnqCbQWY'
API_URL = 'https://gemini.googleapis.com/v1/projects/313270288617/models/gemini-1.5-flash'

def generate_response(pdf_content, user_message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    data = {
        'instances': [
            {
                'pdf_content': pdf_content,
                'user_message': user_message,
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    return result['predictions'][0]['generated_text']