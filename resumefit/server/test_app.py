import pytest
import requests
from flask import Flask
from threading import Thread
import time
from constants import base_resume, job_description

# Import the Flask app
from app import app

# Define the base URL for the Flask app
BASE_URL = "http://localhost:5000"

# Fixture to run the Flask app in a separate thread
@pytest.fixture(scope='module')
def start_flask_app():
    def run_app():
        app.run(debug=True, use_reloader=False)

    thread = Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Give the server time to start
    yield
    # Teardown code can go here if needed

def test_input_resume():
    payload = {
        "base_resume": base_resume,
        "job_description": job_description
    }
    response = requests.post(f"{BASE_URL}/input", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Resume processed successfully"}

def test_output_resume(start_flask_app):
    response = requests.get(f"{BASE_URL}/output")
    assert response.status_code == 200
    assert "customized_resume" in response.json()