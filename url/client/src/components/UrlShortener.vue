<template>
  <div class="container">
    <!-- Centered header -->
    <div class="header">
      <h2>Shortify</h2>
    </div>

    <div class="content">
      <!-- Left section for inputting the long URL -->
      <div class="left-section">
        <input
          v-model="longUrl"
          type="text"
          placeholder="Enter a long URL to shorten"
          class="url-input"
        />
        <button @click="shortenUrl" class="shorten-button">Shorten URL</button>
      </div>

      <!-- Right section to display the shortened URL and short code -->
      <div class="right-section" v-if="shortUrl">
        <h3>Your URL is Ready!</h3>
        <div class="short-url">
          <p>Shortened URL:</p>
          <div class="url-box">
            <a :href="shortUrl" target="_blank">{{ shortUrl }}</a>
            <button @click="copyToClipboard" class="copy-button">Copy</button>
          </div>
        </div>
        <div class="short-code">
          <p>Short Code: <strong>{{ shortCode }}</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      longUrl: '',
      shortUrl: '',
      shortCode: '',
    };
  },
  methods: {
    async shortenUrl() {
      try {
        const response = await axios.post('http://localhost:3001/shorten', { longUrl: this.longUrl });
        this.shortUrl = response.data.shortUrl;
        this.shortCode = response.data.shortCode;
      } catch (error) {
        console.error('Error:', error);
      }
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.shortUrl);
      alert('Short URL copied to clipboard!');
    },
  },
};
</script>

<style scoped>
.container {
  padding: 100px;
  max-width: 900px;
  margin: auto;
  background-color: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.header {
  text-align: center;
  margin-bottom: 50px;
}

.content {
  display: flex;
  justify-content: space-between;
}

.left-section,
.right-section {
  width: 45%;
  padding: 30px;
  border-radius: 8px;
}

.left-section {
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.right-section {
  background-color: #e9ecef;
  text-align: left;
  border-left: 3px solid #6c757d;
  padding-left: 30px;
}

h2, h3 {
  color: #343a40;
  font-weight: bold;
}

.url-input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.shorten-button {
  padding: 10px 20px;
  font-size: 1rem;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.shorten-button:hover {
  background-color: #0056b3;
}

.right-section .short-url,
.right-section .short-code {
  margin-top: 20px;
}

.url-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.short-url a {
  color: #007bff;
  text-decoration: none;
  font-size: 1rem;
  word-break: break-all;
}

.copy-button {
  padding: 5px 10px;
  font-size: 0.9rem;
  color: #fff;
  background-color: #1563b7;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.copy-button:hover {
  background-color: #495057;
}

.short-code p {
  color: #495057;
  font-size: 1rem;
}
</style>
