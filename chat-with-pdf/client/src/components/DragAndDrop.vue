<template>
  <div class="drag-drop-container">
    <h1>Drag and Drop</h1>
    <div class="content">
      <div class="file-list">
        <table>
          <thead>
            <tr>
              <th>TITLE</th>
              <th>ACCESS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pdf, index) in pdfs" :key="index">
              <td>{{ pdf.name }}</td>
              <td>{{ pdf.access.join(', ') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="drag-drop-area" @dragover.prevent @drop.prevent="handleDrop" @click="browseFiles">
        <i class="fas fa-upload"></i>
        <p>Drag and Drop or Click to Browse</p>
      </div>
    </div>
    <input type="file" ref="fileInput" style="display: none;" @change="handleFileSelect" />
    <div v-if="pdfs.length > 0" class="actions">
      <button @click="promptForAccess">Set Access</button>
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
export default {
  data() {
    return {
      pdfs: JSON.parse(localStorage.getItem('pdfs')) || [],
      selectedUsers: [],
      showAccessPrompt: false,
      showChatButton: false,
    };
  },
  methods: {
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
        const pdf = { name: file.name, url: URL.createObjectURL(file), access: [] };
        this.pdfs.push(pdf);
        localStorage.setItem('pdfs', JSON.stringify(this.pdfs));
        this.showAccessPrompt = true;
      } else {
        alert("Please upload a valid PDF file.");
      }
    },
    promptForAccess() {
      this.showAccessPrompt = true;
    },
    setAccess() {
      if (this.selectedUsers.length > 0) {
        this.pdfs[this.pdfs.length - 1].access = this.selectedUsers;
        localStorage.setItem('pdfs', JSON.stringify(this.pdfs));
        this.showAccessPrompt = false;
        this.showChatButton = true;
      } else {
        alert("Please select at least one user.");
      }
    },
    redirectToChat() {
      this.$router.push('/pdf-view-chat');
    }
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

th, td {
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
</style>