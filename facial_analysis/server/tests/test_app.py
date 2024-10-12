import pytest
import json
import base64
from app import app

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def sample_image_path():
    return "/home/vivek/projects/facial_analysis/server/tests/sam1.jpg"

def test_process_image(client, sample_image_path):
    with open(sample_image_path, "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    response = client.post("/process", json={"image": base64_image})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "processed_image" in data

def test_get_processed_image(client):
    # Similar to earlier note: Make sure a previously processed image is available
    response = client.get("/processed")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "image" in data 
