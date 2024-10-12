<template>
  <div>
    <h1 class="title">FREELANCER AUTO BIDDER</h1>
    <!-- Display tokens input if tokens are not submitted -->
    <div v-if="!tokensSubmitted" class="tokens-container">
      <h2 class="sub-title">Enter Tokens</h2>
      <div>
        <label for="oauth_token">OAuth Token:</label>
        <input v-model="oauthToken" type="text" id="oauth_token" placeholder="Enter OAuth Token">
      </div>
      <div>
        <label for="api_key">API Key:</label>
        <input v-model="apiKey" type="text" id="api_key" placeholder="Enter API Key">
      </div>
      <button @click="submitTokens" :disabled="!oauthToken || !apiKey">Submit Tokens</button>
    </div>

    <!-- Display query input if tokens are submitted -->
    <div v-else class="search-container">
      <label for="query">Query:</label>
      <input v-model="query" type="text" id="query" placeholder="Type your query here..." />
      <button @click="handleSearch" :disabled="!isQueryTyped || loading">Search</button>

      <!-- Message for empty query -->
      <p v-if="!isQueryTyped && searchClicked" class="error-message">Please enter a query.</p>

      <!-- Spinner while loading projects -->
      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      loading: false,
      backendUrl: '//172.23.0.170:5000',
      searchClicked: false,
      oauthToken: '',
      apiKey: '',
      tokensSubmitted: false,
    };
  },
  methods: {
    async submitTokens() {
      try {
        const response = await axios.post(`${this.backendUrl}/set_tokens`, {
          oauth_token: this.oauthToken,
          api_key: this.apiKey,
        });
        console.log(response.data.message);
        this.oauthToken = '';
        this.apiKey = '';
        this.tokensSubmitted = true;
      } catch (error) {
        console.error('Error submitting tokens:', error);
      }
    },
    async handleSearch() {
      console.log('Emitting search query:', this.query);
      // Emitting the search query to the parent component
      this.$emit('search-query', this.query);
      this.fetchProjects();
    },
    async fetchProjects() {
      try {
        this.loading = true;
        // Fetch projects based on query
      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        this.loading = false;
      }
    },
  },
  computed: {
    isQueryTyped() {
      return this.query.trim().length > 0;
    },
  },
};
</script>

<style scoped>
/* Spinner container style */
.spinner-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Spinner style */
.spinner {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db; /* Blue */
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* CSS for Tokens input section */
.tokens-container {
  font-family: 'Arial', sans-serif;
  margin: 20px;
  text-align: center;
}

.sub-title {
  color: #4CAF50; /* Green */
}

.tokens-container label {
  margin: 5px;
}

.tokens-container input {
  margin: 5px;
}

.tokens-container button {
  padding: 10px;
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.tokens-container button:disabled {
  background-color: #ccc; /* Light gray */
  color: #666; /* Dark gray */
  cursor: not-allowed;
}

.tokens-container button:hover {
  background-color: #45a049; /* Darker green */
}

/* CSS for Search input section */
.search-container {
  font-family: 'Arial', sans-serif;
  margin: 20px;
  text-align: center;
}

.search-container label {
  margin: 5px;
}

.search-container input {
  margin: 5px;
}

.search-container button {
  padding: 10px;
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-container button:disabled {
  background-color: #ccc; /* Light gray */
  color: #666; /* Dark gray */
  cursor: not-allowed;
}

.search-container button:hover {
  background-color: #45a049; /* Darker green */
}

/* Message style */
.error-message {
  color: red;
  margin-top: 10px;
}

/* Modal style */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

/* Title style */
.title {
  color: #4CAF50; /* Green */
}
</style>
