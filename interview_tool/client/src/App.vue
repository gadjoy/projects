<template>
  <div id="app">
    <header>
      AI Interview Tool
    </header>
    <div id="main-content">
      <div class="question-section">
        <div class="question-box">
        <p v-if="loading">Loading...</p>
        <p v-else>{{ apiResponse }}</p>
          </div>
        </div>
        <div class="mic-button">
          <button @click="handleClick">
            <i class="fas fa-microphone fa-3x"></i>
          </button>
        </div>
        <div class="response-section">
          <div class="transcribed-text">
            {{ transcribedText }}
          </div>
          <div class="feedback">
            {{ feedback }}
          </div>
        </div>
      </div>
    </div>
    <footer>
      Copyright 2024
    </footer>
  <!-- </div> -->
</template>

<script>

import axios from 'axios';

export default {
  name: 'App',

  data() {
    return {
      apiResponse: '',
      loading: true,
      mediaRecorder: null,
      audioChunks: [],
      transcribedText: '',
      feedback: '',
    };
  },

  methods: {
    async handleClick() {
      if (!this.mediaRecorder) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = e => {
          this.audioChunks.push(e.data);
        };
        this.mediaRecorder.start();
      } else {
        this.mediaRecorder.onstop = () => {
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/x-mpeg-3' });
      this.sendAudioToServer(audioBlob);
      this.audioChunks = [];
      this.mediaRecorder = null;
    };
    this.mediaRecorder.stop();
      }
    },
    async sendAudioToServer(audioBlob) {
      const formData = new FormData();
      formData.append('audio', audioBlob);
      try {
        const response = await axios.post('http://localhost:5000/transcribe_blob', formData);
        console.log(response.data.transcription);
        this.transcribedText = response.data.transcription;
        await this.sendTranscribedText();
        // console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
    async sendTranscribedText() {
    try {
      const response = await axios.post('http://localhost:5000/generate_feedback', { text: this.transcribedText });
      this.feedback = response.data.generated_content;
    } catch (error) {
      console.error(error);
    }
  },
  },

  async created() {
    try {
      // const response = await axios.get('https://api.adviceslip.com/advice');
      const response = await axios.get('http://localhost:5000/generate_question');
      // this.apiResponse = response.data.slip.advice;
      this.apiResponse = response.data.generated_question;
      console.log(this.apiResponse);
      this.loading = false;
    } catch (error) {
      console.error(error);
    }
    finally {
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.mic-button button {
  background: none;
  border: none;
  cursor: pointer;
}
</style>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header, footer {
  background-color: #f8d568;
  padding: 20px;
  text-align: center;
  font-weight: bold;
}

#main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.question-section {
  display: flex;
  justify-content: center;
  align-items: center;
  /* position: absolute; */
  top: 0;
  left: 0;
  right: 0;
}

.response-section {
  display: flex;
  flex-direction: row; /* Change to row to display children as columns */
  width: 100%; /* Adjust as needed */
  height: auto; /* Adjust as needed */
  overflow: auto; /* Add scroll bars if the content overflows */
  white-space: pre-wrap; /* Preserve line breaks and spaces */
}

.transcribed-text, .feedback {
  flex: 1; /* Each child will take up equal space */
  height: auto; /* Adjust as needed */
  background-color: #3478f7;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto; /* Add scroll bars if the content overflows */
  white-space: pre-wrap; /* Preserve line breaks and spaces */
  padding: 10px; /* Add some padding */
}
</style>
