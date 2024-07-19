<template>
  <div class="container">

      <!-- Drag and Drop Area Column(FOR ADMIN) -->
      <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6">
        <div class="drag-drop-area" @dragover.prevent @drop.prevent="handleDrop" @click="browseFiles">
          <i class="fas fa-upload"></i>
          <p>Drag and Drop or Click to Browse</p>
        </div>
        <input type="file" ref="fileInput" style="display: none;" @change="handleFileSelect" />
      </div>
    </div>

    <div class="row">
      <!-- Uploaded Files Column -->
      <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6">
        <h2>Uploaded Files</h2>
        <ul>
          <li v-for="file in files" :key="file" class="file-name">{{ file }}</li>
        </ul>
      </div>
    </div>
    <!-- Actions and Access Prompt(ONLY FOR ADMIN) -->
    <div v-if="showAccessPrompt" class="access-prompt">
      <h2>Select Users for Access</h2>
      <div>
        <label>
          <input type="radio" value="user1" v-model="selectedUser" /> User1
        </label>
        <label>
          <input type="radio" value="user2" v-model="selectedUser" /> User2
        </label>
        <button @click="confirmSelection">Confirm Selection</button>
      </div>
    </div>
    <div class="actions">
      <button @click="redirectToChat">Chat</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      pdfs: [],
      selectedUsers: [],
      showAccessPrompt: false,
      showChatButton: false,
      files: [],
      selectedUser: null,
      tempFile: null,
      username: 'admin',
    };
  },
  mounted() {
    this.fetchFiles();
  },
  methods: {
    browseFiles() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.showAccessPrompt = true;
      this.tempFile = file;
      this.files.push(file.name);
      this.pdfs.push(file);
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.showAccessPrompt = true;
      this.tempFile = file;
      this.files.push(file.name);
      this.pdfs.push(file);
    },
    confirmSelection() {
      if (this.selectedUser && !this.selectedUsers.includes(this.selectedUser) && this.tempFile) {
        this.selectedUsers.push(this.selectedUser);
        this.addFile(this.tempFile);
        this.tempFile = null;
        this.showAccessPrompt = false;
        this.selectedUser = null;
      }
      else {
        alert("Please select a user for access.");
      }
    },
    addFile(file) {
      if (file && file.type === "application/pdf") {
        const formData = new FormData();
        formData.append('file', file);
    
        // Ensure a user is selected
        if (this.selectedUser) {
          formData.append('access_username', this.selectedUser);
        } else {
          alert("Please select a user for access.");
          return;
        }
    
        axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
          .then(response => {
            console.log(response.data.message);
            const pdf = { name: file.name, url: URL.createObjectURL(file), access: this.selectedUser };
            this.pdfs.push(pdf);
            localStorage.setItem('pdfs', JSON.stringify(this.pdfs));
            this.fetchFiles();
          })
          .catch(error => {
            console.error("Error uploading file:", error);
          });
      } else {
        alert("Please upload a valid PDF file.");
      }
    },
    fetchFiles() {
      axios.get('http://localhost:5000/files', {
        params: {
          username: this.username
        }
      })
        .then(response => {
          this.files = response.data.files;
        })
        .catch(error => {
          console.error("Error fetching files:", error);
        });
    },
    redirectToChat() {
      this.$router.push('/pdf-view-chat');
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
