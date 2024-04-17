<template>
  <div id="app">
    <h1 class="title">Healthcare AI</h1>
    <div class="conversation" v-if="conversation.length > 0">
      <h2 class="conversation-title">Conversation:</h2>
      <div class="message" v-for="(message, index) in conversation" :key="index" v-html="renderMessage(message)"></div>
    </div>
    <div class="input-container">
      <label for="userQuery" class="input-label">Enter your query:</label>
      <input type="text" id="userQuery" v-model="userQuery" class="input-field">
      <button @click="generateResponse" class="btn">Get Healthcare Response</button>
    </div>
  </div>
</template>

<script>
import showdown from 'showdown';

export default {
  data() {
    return {
      userQuery: '',
      conversation: [],
    }
  },
  methods: {
    generateResponse() {
      fetch('http://127.0.0.1:5000/generate_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_query: this.userQuery })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        this.conversation.push(`**User:** ${this.userQuery}`);
        this.conversation.push(`**Healthcare AI:** ${data.healthcare_response}`);
        this.userQuery = ''; // Clear input after sending query
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    renderMessage(message) {
      const converter = new showdown.Converter();
      return converter.makeHtml(message);
    }
  }
}
</script>

<style scoped>
#app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #007bff;
}

.conversation-title {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 1.2rem;
  color: #333;
}

.input-container {
  margin-top: 20px;
}

.input-label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
