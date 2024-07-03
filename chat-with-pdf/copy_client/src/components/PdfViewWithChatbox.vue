<template>
    <div class="pdf-view-container">
      <div class="pdf-list">
        <button v-for="(pdf, index) in pdfs" :key="index" @click="selectPdf(pdf)">
          {{ pdf.name }}
          <span v-if="pdf.locked">🔒</span>
        </button>
      </div>
      <div class="pdf-view">
        <iframe v-if="selectedPdf" :src="selectedPdf.url" width="100%" height="100%"></iframe>
        <p v-else>Select a PDF to view</p>
      </div>
      <div class="chatbox">
        <h3>Chatbox</h3>
        <!-- Chatbox implementation will go here -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        pdfs: JSON.parse(localStorage.getItem('pdfs')) || [],
        selectedPdf: null,
      };
    },
    methods: {
      selectPdf(pdf) {
        this.selectedPdf = pdf;
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
  </style>
  