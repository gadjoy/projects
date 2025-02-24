<template>
  <div class="container">
    <div class="header">
      <h2>Shortify</h2>
    </div>

    <div class="content">
      <div class="left-section">
        <input
          v-model="longUrl"
          type="text"
          placeholder="Enter a long URL to shorten"
          class="url-input"
        />
        <button @click="shortenUrl" class="shorten-button">Shorten URL</button>
      </div>

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
        const response = await axios.post('https://shortify-tqlk.onrender.com/shorten', { longUrl: this.longUrl });
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
  padding: 40px 20px;
  max-width: 800px;
  margin: auto;
  background-color: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

h2, h3 {
  color: #343a40;
  font-weight: bold;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.left-section,
.right-section {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.left-section {
  background-color: #fff;
}

.right-section {
  background-color: #e9ecef;
}

.url-input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.shorten-button {
  margin-top: 10px;
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

/* Media Queries */
@media (min-width: 768px) {
  .content {
    flex-direction: row;
    justify-content: space-between;
  }
  .left-section,
  .right-section {
    width: 45%;
  }
}
</style>
