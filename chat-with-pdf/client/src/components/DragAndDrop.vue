<template>
  <div class="container">
    <div class="row">
      <!-- Uploaded Files Column -->
      <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6">
        <h2>Uploaded Files</h2>
        <ul>
          <li v-for="file in files" :key="file" class="file-name">{{ file }}</li>
        </ul>
      </div>

      <!-- Drag and Drop Area Column(FOR ADMIN) -->
      <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6">
        <div class="drag-drop-area" @dragover.prevent @drop.prevent="handleDrop" @click="browseFiles">
          <i class="fas fa-upload"></i>
          <p>Drag and Drop or Click to Browse</p>
        </div>
        <input type="file" ref="fileInput" style="display: none;" @change="handleFileSelect" />
      </div>
    </div>

    <!-- Actions and Access Prompt(ONLY FOR ADMIN) -->
    <div v-if="pdfs.length > 0" class="actions">
      <button @click="promptForAccess">Set Access</button>
      <button @click="clearUploads">Clear All Files</button>
      <button v-if="showChatButton" @click="redirectToChat">Chat with PDF</button>
    </div>
    <div v-if="showAccessPrompt" class="access-prompt">
      <h2>Select Users for Access</h2>
      <label><input type="checkbox" value="USER1" v-model="selectedUsers" /> User1</label>
      <label><input type="checkbox" value="USER2" v-model="selectedUsers" /> User2</label>
      <button @click="setAccess">Set Access</button>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      pdfs: JSON.parse(localStorage.getItem('pdfs')) || [],
      selectedUsers: [],
      showAccessPrompt: false,
      showChatButton: false,
      files: [],
    };
  },
  mounted() {
    this.fetchFiles();
  },
  methods: {
    fetchFiles() {
      axios.get('http://localhost:5000/files')
        .then(response => {
          // Handle success
          this.files = response.data.files;
        })
        .catch(error => {
          // Handle error
          console.error("Error fetching files:", error);
        });
    },
    browseFiles() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.addFile(file);
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.addFile(file);
    },
    addFile(file) {
      if (file && file.type === "application/pdf") {
        const formData = new FormData();
        formData.append('file', file);

        axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
          .then(response => {
            // Handle success
            console.log(response.data.message);
            const pdf = { name: file.name, url: URL.createObjectURL(file), access: [] };
            this.pdfs.push(pdf);
            localStorage.setItem('pdfs', JSON.stringify(this.pdfs));
            this.showAccessPrompt = true;
          })
          .catch(error => {
            // Handle error
            console.error("Error uploading file:", error);
          });
      } else {
        alert("Please upload a valid PDF file.");
      }
      this.fetchFiles();
    },
    promptForAccess() {
      this.showAccessPrompt = true;
    },
    setAccess() {
      if (this.selectedUsers.length > 0) {
        const lastPdf = this.pdfs[this.pdfs.length - 1];
        lastPdf.access = this.selectedUsers;

        // Update the local storage
        localStorage.setItem('pdfs', JSON.stringify(this.pdfs));

        // Send the access data to the backend
        axios.post('http://localhost:5000/set-access', {
          pdfName: lastPdf.name,
          access: this.selectedUsers
        })
          .then(response => {
            // Handle success
            console.log(response.data.message);
            this.showAccessPrompt = false;
            this.showChatButton = true;
          })
          .catch(error => {
            // Handle error
            console.error("Error setting access:", error);
          });
      } else {
        alert("Please select at least one user.");
      }
    },
    redirectToChat() {
      this.$router.push('/pdf-view-chat');
    },
    clearUploads() {
      axios.post('/clear-uploads')
        .then(response => {
          console.log(response.data.message);
          this.fetchFiles(); // Refresh the file list
        })
        .catch(error => {
          console.error("Error clearing files:", error);
        });
    },


  }
};
</script>

<style scoped>
.drag-drop-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #3b5998;
  color: #ffffff;
  height: 100vh;
}

h1 {
  margin-bottom: 20px;
}

.content {
  display: flex;
  width: 80%;
  justify-content: space-between;
}

.file-list {
  flex: 1;
}

.drag-drop-area {
  flex: 1;
  width: 300px;
  height: 200px;
  background-color: #000000;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 20px;
}

.drag-drop-area i {
  font-size: 48px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ffffff;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #555555;
}

td {
  background-color: #777777;
}

.actions {
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #f1f1f1;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

button:hover {
  background-color: #ddd;
}

.access-prompt {
  background-color: #f1f1f1;
  color: #000;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.file-name {
  word-wrap: break-word;
  white-space: pre-wrap;
  /* This will wrap the text and preserve whitespace and line breaks */
}
</style>
