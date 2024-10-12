<template>
    <div>
      <!-- Info button in the right-side upper corner -->
      <div class="info-button" @click="showAbout">
        <i class="fas fa-info-circle"></i>
      </div>
  
      <!-- About component -->
      <AboutModal v-if="showAboutModal" @close="hideAbout" 
                  :frontendVersion="frontendVersion" 
                  :frontendModifiedDate="frontendModifiedDate" 
                  :buildNumber="buildNumber" 
                  :backendVersion="backendVersion" 
                  :backendModifiedDate="backendModifiedDate" 
                  :backendUrl="backendUrl"/>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AboutModal from '@/components/AboutModal.vue'; // Adjust the path as per your project structure
  
  export default {
    components: {
      AboutModal,
    },
    data() {
      return {
        backendVersion: '',
        backendModifiedDate: '',
        frontendVersion: 'v1.0.0',
        frontendModifiedDate: '01-04-2024',
        buildNumber: '001',
        showAboutModal: false,
        backendUrl: 'http://127.0.0.1:5000', // Adjust as per your backend URL
      };
    },
    methods: {
      showAbout() {
        this.showAboutModal = true;
        this.fetchBackendVersion();
      },
      hideAbout() {
        this.showAboutModal = false;
      },
      async fetchBackendVersion() {
        try {
          const response = await axios.get(`${this.backendUrl}/version`);
          this.backendVersion = response.data.backend_version;
          this.backendModifiedDate = response.data.backend_modified_date;
        } catch (error) {
          console.error('Error fetching backend version:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styles for this component */
  .info-button {
    position: absolute;
    top: 20px;
    right: 20px;
    cursor: pointer;
    color: #3498db;
    z-index: 999;
  }
  
  .info-button i {
    font-size: 24px;
  }
  </style>
  