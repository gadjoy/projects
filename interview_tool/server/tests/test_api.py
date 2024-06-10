import requests

def test_generate_question_api():
    url = 'http://localhost:5000/generate_question'
    response = requests.get(url)
    print('Question Generation API Response:', response.status_code, response.json())

    # Assert that the request was successful
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def test_transcription_api():
    file_path = '/home/vivek/projects/interview_tool/server/media/mamta.mp4'
    url = 'http://localhost:5000/transcribe'
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    print('Transcription API Response:', response.status_code, response.json())
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    return response.json()

def test_feedback_generation_api():
    transcription_response = test_transcription_api()
    transcription_text = transcription_response['transcription']
    url = 'http://localhost:5000/generate_feedback'
    headers = {'Content-Type': 'application/json'}
    data = {'text': transcription_text}
    response = requests.post(url, json=data, headers=headers)
    print('Content Generation API Response:', response.status_code, response.json())

    # Assert that the request was successful
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"