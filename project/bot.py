import os
import requests
from dotenv import load_dotenv
import time

# Load API key from environment variable
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

# Define the API endpoint
endpoint = "https://generativelanguage.googleapis.com/v1beta2"

def get_response(user_query):
    # Create a well-structured prompt
    prompt = f"""
    Role: You are an AI assistant with a strong understanding of various topics. Your goal is to provide clear, concise, and informative responses to user queries in a conversational manner.

    Context: The user has asked a question. You should provide a detailed and knowledgeable answer based on the information you have. Make sure your response is helpful and easy to understand.

    User Query: {user_query}

    Response:
    """

    # Prepare the request body
    request_body = {
        "prompt": {
            "text": prompt
        }
    }

    # Function to get response from the API
    try_count = 0
    while try_count < 3:  # Retry up to 3 times
        try:
            response = requests.post(f"{endpoint}/models/text-bison-001:generateText?key={api_key}", json=request_body)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            if 'candidates' in data and data['candidates']:
                answer = data['candidates'][0].get('output', '').strip()
                return answer
            
            return "I'm sorry, I couldn't generate a response. Please try again."

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            try_count += 1
            time.sleep(0.5)  # Wait for 0.5 seconds before retrying
    
    return "Failed to get a response after several attempts. Please try again later."

# Example of usage
def main():
    print("Hello! I am your AI assistant. How can I assist you today?")
    
    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit']:
            print("AI: Goodbye! Have a great day!")
            break
        
        response = get_response(user_query)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()
