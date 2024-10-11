import os, json
from dotenv import load_dotenv
from openai import OpenAI
from components.constants import prompt


# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('API_KEY')

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def process_resume_with_openai(resume, job_description):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "assistant", 
             "content": prompt},
            {
                "role": "user",
                "content": f"Write this base resume {resume} to match the following job description: {job_description}"
            }
        ]
    )

    return completion.choices[0].message

