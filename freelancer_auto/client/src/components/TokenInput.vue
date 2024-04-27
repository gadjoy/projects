<template>
<h2>Enter Tokens</h2>
<div>
  <label for="oauth_token">OAuth Token:</label>
  <input v-model="oauthToken" type="text" id="oauth_token" placeholder="Enter OAuth Token">
</div>
<div>
  <label for="api_key">API Key:</label>
  <input v-model="apiKey" type="text" id="api_key" placeholder="Enter API Key">
</div>
<button @click="submitTokens" :disabled="!oauthToken || !apiKey">Submit Tokens</button>
</template>

<script>
import axios from 'axios';
data() {
    return {
      oauthToken: '', // Added OAuth Token data property
      apiKey: '', // Added API Key data property
      tokensSubmitted: false, // Flag to track if tokens are submitted
    },
};
methods: {
    async submitTokens() {
      try {
        const response = await axios.post(`${this.backendUrl}/set_tokens`, {
          oauth_token: this.oauthToken,
          api_key: this.apiKey,
        });
        console.log(response.data.message);
        // Optionally, you can clear the input fields after successful submission
        this.oauthToken = '';
        this.apiKey = '';
        // Set tokensSubmitted to true after successful submission
        this.tokensSubmitted = true;
      } catch (error) {
        console.error('Error submitting tokens:', error);
      }
    }
};