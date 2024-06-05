import requests
from flask import request

# Now you can pass `file_in_bytes` to the OpenAI API

server = "http://127.0.0.1:5000/"

# For sending an audio file for transcription
file_path = '/home/vivek/projects/interview_tool/mamta.mp4'
def transcribe_audio(file_path):
    url = server + 'transcribe'
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    return response.json()

transcribe_audio(file_path)
# file_path = '/path/to/your/file.mp4'
# url = server + 'transcribe'
# files = {'file': open(file_path, 'rb')}
# response = requests.post(url, files=files)
# print("Transcription:", response.json())

# Assuming you have the transcription text, send it for content generation
# transcription_text = 'Your transcribed text here'
# url = server + 'generate_content'
# data = {'text': transcription_text}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# print("Generated Content:", response.json())
