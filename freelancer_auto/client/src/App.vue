<template>
    <div>
      <h1>FREELANCER AUTO BIDDER</h1>
      <AboutModal></AboutModal>
    </div>
  </template>
  
  <script>
  import AboutModal from './components/AboutModal.vue';
  
  export default {
    components: {
      AboutModal,
    },
  };
  </script>

<style scoped>
/* Container style */
div {
  font-family: 'Arial', sans-serif;
  margin: 20px;
  text-align: center;
}

h1 {
  color: #4CAF50;
}


</style>