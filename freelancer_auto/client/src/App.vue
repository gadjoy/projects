<template>
  <div>
    <h1>FREELANCER AUTO BIDDING</h1>

    <div>
      <label for="query">Query:</label>
      <input v-model="query" type="text" id="query" />
      <!-- <label for="searchLimit">Search Limit:</label> -->
      <!-- <input v-model.number="searchLimit" type="number" id="searchLimit" /> -->
      <button @click="fetchProjects" :disabled="loading">Search</button>

      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>
    </div>

    <div v-if="!loading && projects.length > 0">
      <table>
        <!-- Table headers -->
        <thead>
          <tr>
            <th>Select</th>
            <th v-for="header in projectHeaders" :key="header">{{ header }}</th>
            <th>Bid Amount</th>
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <tr v-for="project in projects" :key="project.id">
            <!-- Checkbox for selection -->
            <td>
              <input type="checkbox" v-model="selectedProjects" :value="project.id" />
            </td>
            <!-- Display project data -->
            <td v-for="header in projectHeaders" :key="header">
              {{ project[header] || 'Not available' }}
            </td>
            <!-- Input for bid amount -->
            <td>
              <input v-model="bidAmounts[project.id]" type="number" />
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Buttons for preview and submit -->
      <div>
        <button @click="previewBid">Preview</button>
        <button @click="submitBid">Submit</button>
      </div>

      <!-- Display Preview -->
      <div v-if="preview" class="preview-container">
        <h2>Preview:</h2>
        <table>
          <thead>
            <tr>
              <th>Key</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, key) in preview" :key="key">
              <td>{{ key }}</td>
              <td>{{ value || 'Not available' }}</td>
            </tr>
          </tbody>
        </table>
        <!-- Confirmation button -->
        <button @click="confirmBid">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      searchLimit: '',
      projects: [],
      selectedProjects: [],
      bidAmounts: {},
      loading: false, // Add loading state
      backendUrl: 'http://127.0.0.1:5000',
      preview: null,
      projectHeaders: [
        'id',
        'title',
        'seo_url',
        'submitdate',
        'budget_minimum',
        'budget_maximum',
        'currency_code',
        'currency_exchange_rate',
        'bid_stats_bid_count',
        'bid_stats_bid_avg',
        'budget_maximum_usd',
        'budget_minimum_usd',
        'description',
        'proposal'
      ],
    };
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true; // Set loading state to true
        const response = await axios.get(`${this.backendUrl}/search_projects`, {
          params: {
            query: this.query,
          },
        });

        this.projects = response.data;

      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        this.loading = false; // Set loading state to false
      }
    },
    previewBid() {
      if (this.selectedProjects.length === 0) {
        this.preview = 'No projects selected.';
        return;
      }

      this.preview = {};

      this.selectedProjects.forEach((projectId) => {
        const project = this.projects.find((p) => p.id === projectId);
        const bidAmount = this.bidAmounts[projectId] || 'Not specified';

        this.projectHeaders.forEach((header) => {
          this.preview[header] = project[header] || 'Not available';
        });

        this.preview.bidAmount = bidAmount;
      });
    },
    submitBid() {
      console.log('Submitting bids:', this.selectedProjects, this.bidAmounts);

      // You can add logic here to send bid details to the backend
    },
  },
};
</script>

<style scoped>
  /* Spinner container style */
.spinner-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Spinner style */
.spinner {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db; /* Blue */
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
  /* Container style */
  div {
    font-family: 'Arial', sans-serif;
    margin: 20px;
    text-align: center;
  }
/* Preview container style */
.preview-container {
    border: 1px solid #ddd;
    padding: 10px;
    margin-top: 20px;
}
  h1 {
    color: #4CAF50;
  }

  /* Input and button style */
  label,
  input,
  button {
    margin: 5px;
  }

  /* Table style */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
  }

  th {
    background-color: #f2f2f2;
  }
  /* Checkbox and bid amount input style */
  input[type="checkbox"],
  input[type="number"] {
    margin: 0;
  }

  /* Button container style */
  div > div {
    margin-top: 10px;
  }

  /* Preview and Submit button style */
  button {
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button:hover {
    background-color: #45a049;
  }

  /* Display Preview style */
  h2 {
    color: #4CAF50;
  }

  p {
    margin-top: 10px;
  }
</style>
