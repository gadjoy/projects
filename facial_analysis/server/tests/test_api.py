import requests
import json
import base64

API_BASE_URL = "http://127.0.0.1:5000"  # Assuming your app runs locally
SAMPLE_IMAGE_PATH = "/home/vivek/projects/facial_analysis/server/tests/sam1.jpg"

def test_process_and_retrieve():
    # 1. Process the image
    with open(SAMPLE_IMAGE_PATH, "rb") as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    process_response = requests.post(f"{API_BASE_URL}/process", json={"image": base64_image})
    assert process_response.status_code == 200

    processed_data = process_response.json()
    assert "processed_image" in processed_data

    # 2. Retrieve the processed image
    get_response = requests.get(f"{API_BASE_URL}/processed")
    assert get_response.status_code == 200

    retrieved_data = get_response.json()
    assert "image" in retrieved_data

if __name__ == "__main__":
    test_process_and_retrieve()
