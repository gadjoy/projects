<template>
  <div class="chat">
    <div v-for="message in messages" :key="message.id" class="message">
      {{ message.text }}
    </div>
    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message...">
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      messages: [],
      newMessage: ''
    };
  },
  methods: {
    sendMessage() {
      this.messages.push({ id: Date.now(), text: this.newMessage });
      axios.get('/get', { params: { msg: this.newMessage } })
        .then(response => {
          this.messages.push({ id: Date.now(), text: response.data });
        })
        .catch(error => {
          console.error('Error sending message:', error);
        });
      this.newMessage = '';
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>














