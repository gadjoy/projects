<template>
  <div class="login">
    <h2>Login</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div>
      <label for="username">Username:</label>
      <input id="username" type="text" v-model="username" />
    </div>
    <div>
      <label for="password">Password:</label>
      <input id="password" type="password" v-model="password" />
    </div>
    <button @click="login">Login</button>
  </div>
</template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '', // To display login errors
      };
    },
    methods: {
      login() {
        axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password
        })
        .then(response => {
        // Handle response
        console.log(response.data.message); // Logged in
        localStorage.setItem('username', this.username); // Store username in localStorage
        localStorage.setItem('role', response.data.role);
        if (response.data.role === 'admin') {
          this.$router.push('/drag-and-drop');
        } else {
          this.$router.push('/pdf-view-chat');
        }
      })
        .catch(error => {
          // Handle error
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.log(error.response.data);
            console.log(error.response.status);
            this.errorMessage = error.response.data.message || 'An error occurred. Please try again.';
          } else if (error.request) {
            // The request was made but no response was received
            console.log(error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message);
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .login {
    text-align: center;
    background-color: #1c6ea4;
    color: white;
    padding: 40px;
    border-radius: 10px;
    width: 300px;
    margin: 0 auto;
    margin-top: 20vh;
  }
  input {
    display: block;
    margin: 10px auto;
    padding: 10px;
    width: 200px;
    border-radius: 10px;
    border: none;
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
  </style>
  