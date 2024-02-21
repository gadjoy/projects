<template>
  <div id="app">
    <h1>Chat Bot Tester</h1>
    <textarea type="text" v-model="userInput" placeholder="Enter your text here" class="input-box"></textarea>  
    <button @click="sendRequest">Generate</button>
    <select class="dropdown">
      <option disabled selected>Test Case Type</option>
      <!-- Add your options here -->
    </select>
    <select class="dropdown">
      <option disabled selected>Error Classification</option>
      <!-- Add your options here -->
    </select>
    <h3>Generated Test Scenarios & Test Cases</h3>
    <div class="output-box" v-html="markdownOutput"></div>
  </div>
</template>

<script>
import showdown from 'showdown';
import axios from 'axios';

export default {
  data() {
    return {
      userInput: '',
      markdownOutput: ''
    }
  },
  methods: {
    async sendRequest() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/generate', {
          prompt: this.userInput
        });
        this.markdownOutput = this.converter.makeHtml(response.data.content); 
      } catch (error) {
        console.error("Error sending request:", error); 
        // Handle the error (e.g., display an error message)
      }
    }
  },
  mounted() {
   this.converter = new showdown.Converter();
  },
  // watch: {
  //   userInput() {
  //     this.markdownOutput = this.converter.makeHtml(this.userInput);
  //   }
  // }
}
</script>

<style>
.input-box {
  width: 100%;
  height: 250px; /* Adjust as needed */
  padding: 10px;
  box-sizing: border-box;
}
.dropdown {
  display: block;
  /* width: 100%; */
  margin-top: 10px;
}
.output-box {
  margin-top: 10px;
  border: 1px solid #ccc;
  padding: 15px;
}
</style>