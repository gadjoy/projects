<template>
  <div>
    <div class="info-button" @click="toggleModal">
      <i class="fas fa-info-circle">About</i>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="toggleModal">&times;</span>
        <h2>About</h2>
        <p>freelancer-auto-bidder@{{ frontendVersion }} &nbsp; Build: {{ buildNumber }}</p>
        <p>{{ localFrontendModifiedDate }}</p>
        <br>
        <a :href="backendUrl">{{ backendUrl }}</a>
        {{ localBackendVersion }}
        {{ localBackendModifiedDate }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      backendUrl: 'http://127.0.0.1:5000',
      backendVersion: '',
      backendModifiedDate: '',
      frontendVersion: 'v1.0.0',
      frontendModifiedDate: '01-04-2024',
      buildNumber: '001',
      showModal: false,
      localBackendVersion: '',
      localBackendModifiedDate: '',
      localFrontendModifiedDate: '01-04-2024',
    };
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
      if (this.showModal) {
        this.fetchBackendVersion();
        this.fetchFrontendModifiedDate();
      }
    },
    async fetchBackendVersion() {
      try {
        const response = await axios.get(`${this.backendUrl}/version`);
        this.localBackendVersion = response.data.backend_version;
        this.localBackendModifiedDate = response.data.backend_modified_date;
      } catch (error) {
        console.error('Error fetching backend version:', error);
      }
    },
    fetchFrontendModifiedDate() {
      this.localFrontendModifiedDate = '01-04-2024';
    },
  },
};
</script>

<style scoped>
/* Modal style */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

/* Optional: Style the info button for positioning */
.info-button {
  position: absolute; /* Makes the button absolute positioned */
  top: 10px; /* Positions 10px from the top */
  left: 10px; /* Positions 10px from the left */
}
</style>
