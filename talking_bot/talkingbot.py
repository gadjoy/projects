import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import queue
import threading
import requests
import time
import subprocess
import tempfile
import os
from pygame import mixer
import wave

class VoiceAssistant:
    def __init__(self, 
                 model_path="vosk-model-small-en-us", 
                 ollama_url="http://localhost:11434",
                 max_tokens=100,
                 piper_model="en_GB-alan-low.onnx"):
        """
        Initialize the voice assistant
        Args:
            model_path (str): Path to the Vosk model
            ollama_url (str): URL of the Ollama API
            max_tokens (int): Maximum tokens for Ollama response
            piper_model (str): Name of the Piper voice model
        """
        # Audio settings for input
        self.samplerate = 16000
        self.blocksize = 8000
        self.device = 0
         
        # Initialize Vosk
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        
        # Queue for audio blocks
        self.q = queue.Queue()
        
        # Control flag
        self.running = False

        # Ollama settings
        self.ollama_url = ollama_url
        self.last_request_time = 0
        self.min_request_interval = 2
        self.max_tokens = max_tokens

        # Piper settings
        self.piper_model = piper_model
        
        # Initialize pygame mixer for audio playback
        mixer.init()

    def text_to_speech(self, text):
        """Convert text to speech using Piper and play it"""
        try:
            # Create a temporary file for the WAV output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav_path = temp_wav.name

            """
            echo 'The human brain, like any other complex organ, has been extensively studied and mapped by scientists over the years.' | /home/dietpi/piper/piper --model en_GB-alan-low.onnx --output-raw | aplay -D plug:default -r 22050 -f S16_LE -t raw -c 1 -
            """
            # Run Piper TTS command to generate WAV file
            piper_command = f"echo '{text}' | /home/dietpi/piper/piper --model {self.piper_model} --output_file {temp_wav_path}"
            subprocess.run(piper_command, shell=True, check=True)

            # Play the generated WAV file
            play_command = f"aplay {temp_wav_path}"
            subprocess.run(play_command, shell=True, check=True)

            # Clean up temporary file
            os.unlink(temp_wav_path)

        except subprocess.CalledProcessError as e:
            print(f"Error in text to speech: {str(e)}")
        except Exception as e:
            print(f"Unexpected error in text to speech: {str(e)}")

    def send_to_ollama(self, text):
        """Send text to Ollama API and get response"""
        current_time = time.time()
        
        if current_time - self.last_request_time < self.min_request_interval:
            return
        
        try:
            endpoint = f"{self.ollama_url}/api/generate"
            payload = {
                "model": "smollm:135m",
                "prompt": text + ". Respond in one sentence.",
                "stream": False,
                "options": {
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if 'response' in result:
                response_text = result['response']
                print(f"Ollama response: {response_text}")
                # Convert response to speech
                self.text_to_speech(response_text)
            
            self.last_request_time = current_time
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {str(e)}")
        except json.JSONDecodeError:
            print("Error parsing Ollama response")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    def audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice to handle audio blocks"""
        if status:
            print(status)
        self.q.put(bytes(indata))

    def process_audio(self):
        """Process audio from the queue and perform recognition"""
        while self.running:
            data = self.q.get()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if result["text"]:
                    recognized_text = result["text"]
                    print(f"Recognized: {recognized_text}")
                    # Send recognized text to Ollama
                    self.send_to_ollama(recognized_text)
            else:
                partial = json.loads(self.recognizer.PartialResult())
                if partial["partial"]:
                    print(f"Partial: {partial['partial']}")

    def start_listening(self):
        """Start listening to audio input"""
        self.running = True
        
        # Start processing thread
        processing_thread = threading.Thread(target=self.process_audio)
        processing_thread.start()
        
        # Start audio stream
        with sd.RawInputStream(samplerate=self.samplerate,
                             blocksize=self.blocksize,
                             device=self.device,
                             dtype=np.int16,
                             channels=1,
                             callback=self.audio_callback):
            print("Listening... Press Ctrl+C to stop")
            while self.running:
                sd.sleep(100)

    def stop_listening(self):
        """Stop listening and processing"""
        self.running = False
        self.q.put(None)
        mixer.quit()

def main():
    # First, ensure you have the necessary components installed:
    # 1. Piper TTS: https://github.com/rhasspy/piper
    # 2. A Piper voice model
    
    try:
        # Initialize voice assistant
        assistant = VoiceAssistant(
            ollama_url="http://localhost:11434",
            max_tokens=100,
            piper_model="en_GB-alan-low.onnx"  # Replace with your preferred voice model
        )
        
        # Start listening
        assistant.start_listening()
        
    except KeyboardInterrupt:
        print("\nStopping...")
        assistant.stop_listening()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()