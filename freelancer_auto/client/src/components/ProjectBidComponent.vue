<template>
  <div>
    <!-- Display spinner while loading -->
    <div v-if="loading" class="spinner-container">
      <div class="spinner"></div>
    </div>

    <!-- Display projects table here -->
    <table v-if="projects.length > 0" class="projects-table">
      <thead>
        <tr>
          <th v-for="header in projectHeaders" :key="header">{{ header }}</th>
          <th>Select</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="project in projects" :key="project.id">
          <td>{{ project.id }}</td>
          <td>{{ project.title }}</td>
          <td>{{ project.seo_url }}</td>
          <td>{{ formatDate(project.submitdate) }}</td>
          <td>{{ project.budget_minimum }}</td>
          <td>{{ project.budget_maximum }}</td>
          <td>{{ project.currency_code }}</td>
          <td>{{ project.bid_stats_bid_count }}</td>
          <td>{{ project.bid_stats_bid_avg }}</td>
          <td>{{ project.budget_maximum_usd }}</td>
          <td>{{ project.budget_minimum_usd }}</td>
          <td>
            <button @click="openModal(project)">View Description</button>
          </td>
          <td>
            <input type="checkbox" v-model="selectedProjects" :value="project.id" />
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No projects available.</p>
    </div>

    <!-- Description Modal -->
    <div v-if="descriptionModalOpen" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>{{ selectedProjectDescription }}</p>
      </div>
    </div>

    <!-- Preview Modal -->
    <!-- Modal content -->

    <!-- Preview button -->
    <button @click="previewBid" :disabled="selectedProjects.length === 0">Preview</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      projects: [],
      selectedProjects: [],
      loading: false, // Track loading state
      backendUrl: '//172.23.0.170:5000',
      preview: [],
      previewModalOpen: false,
      selectedProjectDescription: '',
      projectHeaders: [
        'id',
        'title',
        'seo_url',
        'submitdate',
        'budget_minimum',
        'budget_maximum',
        'currency_code',
        'bid_stats_bid_count',
        'bid_stats_bid_avg',
        'budget_maximum_usd',
        'budget_minimum_usd',
        'description',
      ],
      descriptionModalOpen: false,
    };
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true; // Set loading to true while fetching data
        const response = await axios.get(`${this.backendUrl}/search_projects`, {
          params: {
            query: this.searchQuery,
          },
        });
        this.projects = response.data;
      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        this.loading = false; // Set loading to false after data is fetched
      }
    },
    async generateAndShowProposal(id) {
      try {
        const response = await axios.get(`${this.backendUrl}/generate_proposal`, {
          params: {
            project_id: id,
          },
        });
        return response.data.proposal || 'No proposal available';
      } catch (error) {
        console.error('Error generating proposal:', error);
        return 'Failed to generate proposal. Please try again later.';
      }
    },
    async previewBid() {
      if (this.selectedProjects.length === 0) {
        this.preview = [];
        return;
      }
      this.preview = [];
      for (const projectId of this.selectedProjects) {
        const project = this.projects.find((p) => p.id === projectId);
        const proposal = await this.generateAndShowProposal(project.id);
        this.preview.push({ ...project, description: proposal });
      }
      // Open preview modal after generating preview
      this.previewModalOpen = true;
    },
    submitBid() {
      console.log('Submitting bids:', this.selectedProjects);
      // You can add logic here to send bid details to the backend
      // this.createBid();
      this.closeModal();
    },
    openModal(project) {
  this.selectedProjectDescription = project.description || 'No description available'; // Assign project description or a default message
  this.descriptionModalOpen = true; // Set description modal to open
},

    closeModal() {
      this.descriptionModalOpen = false;
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
  },
  computed: {
    canConfirmBid() {
      return this.preview && this.preview.length > 0;
    },
  },
  watch: {
    searchQuery() {
      // Fetch projects whenever the search query changes
      this.fetchProjects();
    },
  },
  created() {
    // Fetch projects when the component is created
    this.fetchProjects();
  },
};
</script>

<style scoped>
/* Styles for the spinner */
.spinner-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000; /* Ensure spinner is on top */
}

.spinner {
  border: 5px solid #f3f3f3; /* Light grey */
  border-top: 5px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite; /* Spin animation */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Modal styles */
.modal {
  display: none; /* Hidden by default */
  position: fixed;
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* Close Button */
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
</style>
