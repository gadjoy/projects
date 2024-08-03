<template>
  <div class="pdf-view-container">
    <div class="pdf-list">
      <button v-for="(pdf, index) in pdfs" :key="index" @click="selectPdf(pdf)">
        {{ pdf }}
      </button>
    </div>
    <div class="pdf-view">
      <iframe v-if="selectedPdf" :src="`http://localhost:5000/retreive/${selectedPdf}`" width="100%" height="100%"></iframe>
      <p v-else>Select a PDF to view</p>
    </div>
    <div class="chatbox">
      <h3>Chatbox</h3>
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <strong>{{ message.sender }}:</strong> {{ message.text }}
        </div>
      </div>
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pdfs: [],
      selectedPdf: null,
      userMessage: '',
      messages: [],
    };
  },
  created() {
    this.fetchPdfs();
  },
  methods: {
    fetchPdfs() {
      const username = localStorage.getItem('username'); // Fetch the username from localStorage
      fetch(`http://localhost:5000/files?username=${username}`)
        .then(response => response.json())
        .then(data => {
          this.pdfs = data.files;
        })
        .catch(error => {
          console.error('Error fetching PDFs:', error);
        });
    },
    selectPdf(pdf) {
      this.selectedPdf = pdf;
      this.messages = [];  // Clear messages when a new PDF is selected
    },
    sendMessage() {
      if (this.userMessage.trim() === '') return;

      const pdfContent = this.getPdfContent();
      const userMessage = this.userMessage;

      fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pdf_content: pdfContent, message: userMessage }),
      })
        .then(response => response.json())
        .then(data => {
          this.messages.push({ sender: 'User', text: userMessage });
          this.messages.push({ sender: 'AI', text: data.response });
          this.userMessage = '';
        })
        .catch(error => {
          console.error('Error sending message:', error);
        });
    },
    getPdfContent() {
      // Logic to fetch and return the content of the selected PDF
      // This might involve reading the PDF file and extracting its text content
      return 'PDF content here';
    }
  }
};
</script>

<style scoped>
.pdf-view-container {
  display: flex;
  height: 100vh;
  background-color: #3b5998;
  color: #ffffff;
}

.pdf-list {
  width: 20%;
  background-color: #8b9dc3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pdf-list button {
  margin: 10px 0;
  padding: 10px;
  border: none;
  border-radius: 25px;
  background-color: #000000;
  color: #ffffff;
  cursor: pointer;
}

.pdf-view {
  width: 40%;
  background-color: #3b5998;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbox {
  width: 40%;
  background-color: #000000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.messages {
  flex: 1;
  overflow-y: auto;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.message {
  margin: 5px 0;
}

input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}
</style>
