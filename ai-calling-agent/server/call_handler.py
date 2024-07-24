import requests
import time
import json
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

CALL_LOGS_FILE = "server/call_logs.json"
TRANSCRIPT_FILE = "server/latest_transcription.json"

def make_call(name, phone_number, script_content):
    url = "https://api.aicaller.io/v1/phoneCalls"
    payload = {
        "callTemplateId": os.getenv("CALL_TEMPLATE_ID"),
        "nameOfHuman": name,
        "toPhoneNumber": phone_number,
        "teamId": os.getenv("TEAM_ID"),
        "promptVariableValues": [
            {
                "key": "customer_name",
                "value": name
            }
        ],
        "scriptContent": script_content
    }

    headers = {
        "aicaller-api-key": os.getenv("AICALLER_API_KEY"),
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        logging.debug(f"Response from API: {response.json()}")

        call_id = response.json().get('data', {}).get('_id')
        logging.debug(f"Call ID: {call_id}")

        if not call_id:
            return "Failed to retrieve call ID."

        if wait_for_call_completion(call_id, headers):
            logging.debug("Call completed.")
        transcript = poll_for_transcript(call_id, headers)
        if transcript:
            with open(TRANSCRIPT_FILE, "w") as file:
                json.dump(transcript, file)
            log_call(name, phone_number, call_id)
            return "Call completed and transcript saved."
        else:
            return "Failed to retrieve transcript."

    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            return f"400 Client Error: Bad Request - {response.text}"
        elif response.status_code == 401:
            return "401 Client Error: Unauthorized - Check your API key."
        else:
            return str(e)
    except requests.RequestException as e:
        return str(e)

def wait_for_call_completion(call_id, headers):
    url = f"https://api.aicaller.io/v1/phoneCalls/{call_id}"

    while True:
        try:
            status_response = requests.get(url, headers=headers)
            status_response.raise_for_status()

            status_data = status_response.json()
            logging.debug(f"Call status data: {status_data}")

            if status_data.get('data', {}).get('status') == 'completed':
                return True
            elif status_data.get('data', {}).get('status') == 'failed':
                return False

        except requests.RequestException:
            pass

        time.sleep(5)

def poll_for_transcript(call_id, headers):
    url = "https://api.aicaller.io/v1/transcripts"
    querystring = {"phoneCallId": call_id}

    while True:
        try:
            transcript_response = requests.get(url, headers=headers, params=querystring)
            transcript_response.raise_for_status()

            transcript_data = transcript_response.json()
            logging.debug(f"Transcript data: {transcript_data}")

            if 'data' in transcript_data:
                return transcript_data['data']
        except requests.RequestException:
            pass

        time.sleep(5)

def log_call(name, phone_number, call_id):
    call_log_entry = {
        "name": name,
        "phone_number": phone_number,
        "timestamp": datetime.now().isoformat(),
        "call_id": call_id
    }

    if os.path.exists(CALL_LOGS_FILE):
        with open(CALL_LOGS_FILE, "r") as file:
            call_logs = json.load(file)
    else:
        call_logs = []

    call_logs.append(call_log_entry)

    with open(CALL_LOGS_FILE, "w") as file:
        json.dump(call_logs, file)
