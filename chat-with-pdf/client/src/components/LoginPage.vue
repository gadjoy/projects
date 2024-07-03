<template>
    <div class="login">
      <h2>Login</h2>
      <div>
        <label>Username:</label>
        <input type="text" v-model="username" />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" />
      </div>
      <button @click="login">Login</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        this.$router.push('/drag-and-drop');
        // if (this.username && this.password) {
        //   if (this.username === 'user1' && this.password === 'password1') {
        //     localStorage.setItem('currentUser', 'USER1');
        //     this.$router.push('/drag-and-drop');
        //   } else if (this.username === 'user2' && this.password === 'password2') {
        //     localStorage.setItem('currentUser', 'USER2');
        //     this.$router.push('/drag-and-drop');
        //   } else {
        //     alert('Invalid username or password');
        //   }
        // } else {
        //   alert('Please enter both username and password');
        // }
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
  