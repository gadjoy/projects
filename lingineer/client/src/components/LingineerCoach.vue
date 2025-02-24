<template>
  <div class="container">
    <h1>Lingineer AI Coach</h1>

    <label for="scenario">Choose a Scenario:</label>
    <select v-model="scenario" id="scenario">
      <option value="Team Meeting Simulation">Team Meeting Simulation</option>
      <option value="Technical Explanation">Technical Explanation</option>
      <option value="Presentation Practice">Presentation Practice</option>
      <option value="Pronunciation Practice">Pronunciation Practice</option>
    </select>

    <label v-if="scenario !== 'Pronunciation Practice'" for="message">Your Message:</label>
    <textarea
      v-if="scenario !== 'Pronunciation Practice'"
      v-model="message"
      id="message"
      rows="4"
      placeholder="Type your message here..."
    ></textarea>

    <button v-if="scenario !== 'Pronunciation Practice'" @click="sendMessage" :disabled="isLoading">
      {{ isLoading ? 'Sending...' : 'Send Message' }}
    </button>

    <!-- Pronunciation Practice Section -->
    <div v-if="scenario === 'Pronunciation Practice'" class="pronunciation-section">
      <label>Pronunciation Practice:</label>
      <button @click="playSamplePhrase">Play Sample Phrase</button>
      <button 
        @click="startRecording" 
        v-if="!isRecording" 
        class="record-button">
        Start Recording
      </button>
      <button 
        @click="stopRecording" 
        v-else 
        class="record-button active">
        Stop Recording
      </button>
    </div>

    <!-- Feedback/Error Display -->
    <div v-if="feedback" class="feedback">
      <h3>Feedback</h3>
      <div v-html="formattedFeedback"></div>
    </div>
    <div v-if="audioFeedback" class="feedback">{{ audioFeedback }}</div>
    <div v-if="error" class="error">
      <h3>Error</h3>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      scenario: "Team Meeting Simulation",
      message: "",
      feedback: "",
      audioFeedback: "",
      error: "",
      isLoading: false,
      isRecording: false,
      recorder: null,
      audioBlob: null
    };
  },
  computed: {
    formattedFeedback() {
      let formattedText = this.feedback
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Bold text
        .replace(/^\*/gm, "<li>") // List item for bullet points
        .replace(/(Mistakes:|Corrected sentence:|Suggestions to improve:)/g, "<p><strong>$1</strong></p>") // Bold headings
        .replace(/\n/g, "<br/>"); // Line breaks

      // Wrap bullet points in a <ul> tag for each section
      formattedText = formattedText.replace(/<li>/g, "<ul><li>").replace(/<\/li>(?!<li>)/g, "</li></ul>");

      return formattedText;
    }
  },
  methods: {
    async sendMessage() {
      this.feedback = "";
      this.error = "";
      this.isLoading = true;

      if (!this.message.trim()) {
        this.error = "Please enter a message.";
        this.isLoading = false;
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5001/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            scenario: this.scenario,
            message: this.message
          })
        });

        const data = await response.json();

        if (response.ok) {
          this.feedback = data.feedback;
        } else {
          this.error = data.error || "An error occurred";
        }
      } catch (error) {
        this.error = "Unable to connect to the server.";
      } finally {
        this.isLoading = false;
      }
    },
    playSamplePhrase() {
      const sampleAudio = new Audio("/home/ash93/projects/lingineer/client/public/audio/sample_phrase.mp3 b  ");
      sampleAudio
        .play()
        .catch((error) => {
          this.error = "Unable to play the sample phrase.";
          console.error(error);
        });
    },
    async startRecording() {
      try {
        this.isRecording = true;
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.recorder = new MediaRecorder(stream);
        this.recorder.ondataavailable = (e) => {
          this.audioBlob = e.data; // Save recorded audio
        };
        this.recorder.start();
      } catch (error) {
        this.error = "Unable to access microphone.";
        this.isRecording = false;
      }
    },
    stopRecording() {
      this.recorder.stop();
      this.isRecording = false;
      this.sendAudioFeedback();
    },
    async sendAudioFeedback() {
      const formData = new FormData();
      formData.append("audio", this.audioBlob, "user_recording.wav");

      try {
        const response = await fetch("http://127.0.0.1:5001/pronunciation", {
          method: "POST",
          body: formData
        });
        const data = await response.json();

        if (response.ok) {
          this.audioFeedback = data.feedback;
        } else {
          this.error = data.error || "An error occurred";
        }
      } catch (error) {
        this.error = "Unable to connect to the server.";
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
  text-align: left;
}

select,
textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.record-button {
  background-color: #4caf50;
  color: white;
}

.record-button.active {
  background-color: #f44336;
  color: white;
}

.feedback {
  margin-top: 20px;
  padding: 20px;
  background-color: #e9ffe9;
  border-left: 4px solid #4caf50;
  text-align: left;
  font-size: 16px;
  overflow-y: auto;
}

.error {
  margin-top: 20px;
  padding: 15px;
  background-color: #ffdddd;
  border-left: 4px solid #f44336;
}
</style>
