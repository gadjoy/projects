<template>
  <div id="app">
    <header>AI Interview Tool</header>
    <div id="main-content">
      <div class="question-section">
        <div class="question-box">
          <p v-if="loading">Loading...</p>
          <p v-else>{{ question }}</p>
        </div>
      </div>
      <div class="mic-button">
        <button @click="handleClick">
          <i class="fas fa-microphone fa-3x"></i>
        </button>
        <p v-if="recording">Recording...</p>
      </div>
      <div class="response-section">
        <div class="transcribed-text">
          <p>Transcribed/Text Answer:</p>
          <textarea v-model="transcribedText" rows="5" cols="50"></textarea>
        </div>
        <div class="feedback">
          <button @click="sendTranscribedText">Get Feedback</button>
          <p>Feedback:</p>
          {{ feedback }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',

  data() {
    return {
      question: '',
      loading: true,
      mediaRecorder: null,
      audioChunks: [],
      transcribedText: '',
      feedback: '',
      recording: false,
    };
  },

  methods: {
    async handleClick() {
      if (!this.mediaRecorder) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.mediaRecorder = new MediaRecorder(stream);
          this.mediaRecorder.ondataavailable = e => {
            this.audioChunks.push(e.data);
          };
          this.mediaRecorder.start();
          this.recording = true;
        } catch (err) {
          console.error('Error accessing microphone:', err);
        }
      } else {
        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/mp3' });
          await this.sendAudioToServer(audioBlob);
          this.audioChunks = [];
          this.mediaRecorder = null;
          this.recording = false;
        };
        this.mediaRecorder.stop();
      }
    },

    async sendAudioToServer(audioBlob) {
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.mp3');
      try {
        const response = await axios.post('http://localhost:5000/transcribe', formData);
        this.transcribedText = response.data.transcription;
      } catch (error) {
        console.error('Error sending audio to server:', error);
      }
    },

    async sendTranscribedText() {
      try {
        const response = await axios.post('http://localhost:5000/generate_feedback', { text: this.transcribedText });
        this.feedback = response.data.generated_content;
      } catch (error) {
        console.error('Error sending transcribed text:', error);
      }
    },

    async fetchQuestion() {
      try {
        const response = await axios.get('http://localhost:5000/generate_question');
        this.question = response.data.generated_question;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching question:', error);
      }
    }
  },

  created() {
    this.fetchQuestion();
  }
}
</script>

<style scoped>
.mic-button {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mic-button button {
  background: none;
  border: none;
  cursor: pointer;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
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
  margin-bottom: 20px;
}

.response-section {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.transcribed-text, .feedback {
  flex: 1;
  background-color: #3478f7;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  margin: 5px;
  white-space: pre-wrap;
  overflow: auto;
}

textarea {
  width: 80%;
  padding: 10px;
  margin-top: 10px;
}

button {
  background-color: #f8d568;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #e6c559;
}
</style>
