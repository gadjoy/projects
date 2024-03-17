<template>
  <div>
    <h1>FREELANCER AUTO BIDDING</h1>

    <div>
      <label for="query">Query:</label>
      <input v-model="query" type="text" id="query" />
      <button @click="fetchProjects" :disabled="loading">Search</button>

      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>
    </div>

    <div v-if="!loading && roundedProjects.length > 0">
      <table>
        <!-- Table headers -->
        <thead>
          <tr>
            <th>Select</th>
            <th v-for="header in projectHeaders" :key="header">{{ formatHeader(header) }}</th>
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <tr v-for="project in roundedProjects" :key="project.id">
            <!-- Checkbox for selection -->
            <td>
              <input type="checkbox" v-model="selectedProjects" :value="project.id" />
            </td>
            <!-- Display project data -->
            <td v-for="header in projectHeaders" :key="header">
              <template v-if="header !== 'description'">
                <!-- Check if header is budget_minimum_usd or budget_maximum_usd -->
                <template v-if="header === 'budget_minimum_usd' || header === 'budget_maximum_usd'">
                  ${{ project[header] || 'Not available' }}
                </template>
                <!-- If header is not budget_minimum_usd or budget_maximum_usd -->
                <template v-else-if="header === 'submitdate'">
                  {{ formatDate(project[header]) || 'Not available' }}
                </template>
                <template v-else>
                  {{ project[header] || 'Not available' }}
                </template>
              </template>
              <template v-else>
                <button @click="openModal(project.description)">View Description</button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Buttons for preview and submit -->
      <div>
        <button @click="previewBid" :disabled="selectedProjects.length === 0">Preview</button>
        <button @click="submitBid" :disabled="selectedProjects.length === 0 || !preview">Submit</button>
      </div>

      <!-- Modal window for project description -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <p>{{ modalDescription }}</p>
        </div>
      </div>

      <!-- Modal window for proposal -->
      <div v-if="showProposalModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeProposalModal">&times;</span>
          <p>{{ modalProposal }}</p>
        </div>
      </div>

      <!-- Display Preview -->
      <div v-if="preview" class="preview-container">
        <h2>Preview:</h2>
        <table v-if="selectedProjects.length > 0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>SEO URL</th>
              <th>Submit Date</th>
              <th>Budget Minimum</th>
              <th>Budget Maximum</th>
              <th>Currency Code</th>
              <th>Bid Stats Bid Count</th>
              <th>Bid Stats Bid Avg</th>
              <th>Budget Maximum USD</th>
              <th>Budget Minimum USD</th>
              <th>Description</th>
              <th>Proposal</th>
              <th>Bid Amount</th>
            </tr>
          </thead>
          <tbody>
            <!-- Iterate over preview items -->
            <tr v-for="(item, index) in preview" :key="index">
              <td>{{ item.id }}</td>
              <td>{{ item.title }}</td>
              <td>{{ item.seo_url }}</td>
              <td>{{ formatDate(item.submitdate) }}</td>
              <td>{{ item.budget_minimum }}</td>
              <td>{{ item.budget_maximum }}</td>
              <td>{{ item.currency_code }}</td>
              <td>{{ item.bid_stats_bid_count }}</td>
              <td>{{ parseFloat(item.bid_stats_bid_avg).toFixed(1) }}</td>
              <td>${{ parseFloat(item.budget_maximum_usd).toFixed(0) }}</td>
              <td>${{ parseFloat(item.budget_minimum_usd).toFixed(0) }}</td>
              <td>
                <button @click="openModal(item.description)">View Description</button>
              </td>
              <td>
                <!-- Open modal on click -->
                <button @click="openProposalModal(item.proposal)">View Proposal</button>
              </td>
              <td><input type="number" v-model="item.bidAmount" placeholder="Enter bid amount"></td>
            </tr>
          </tbody>
        </table>
        <p v-else>No projects selected for preview.</p>
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
      loading: false,
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
        'bid_stats_bid_count',
        'bid_stats_bid_avg',
        'budget_maximum_usd',
        'budget_minimum_usd',
        'description',
      ],
      showModal: false,
      modalDescription: '',
      showProposalModal: false,
      modalProposal: ''
    };
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true;
        const response = await axios.get(`${this.backendUrl}/search_projects`, {
          params: {
            query: this.query,
          },
        });

        this.projects = response.data;

      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        this.loading = false;
      }
    },
    openModal(description) {
      this.showModal = true;
      this.modalDescription = description;
    },
    closeModal() {
      this.showModal = false;
      this.modalDescription = '';
    },
    openProposalModal(proposal) {
      this.showProposalModal = true;
      this.modalProposal = proposal;
    },
    closeProposalModal() {
      this.showProposalModal = false;
      this.modalProposal = '';
    },
    async generateAndShowProposal(id) {
      try {
        const response = await axios.get(`${this.backendUrl}/generate_proposal`, {
          params: {
            project_id: id,  // Send project ID as a query parameter
          },
        });
        return response.data.proposal || 'No proposal available';
      } catch (error) {
        console.error('Error generating proposal:', error);
        return 'No proposal available';
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
        const previewItem = {};

        this.projectHeaders.forEach((header) => {
          previewItem[header] = project[header] || 'Not available';
        });

        previewItem.bidAmount = ''; // Initialize bid amount property

        // Call generateAndShowProposal method for each selected project
        previewItem.proposal = await this.generateAndShowProposal(projectId);

        this.preview.push(previewItem);
      }
    },
    submitBid() {
      console.log('Submitting bids:', this.selectedProjects);
      // You can add logic here to send bid details to the backend
      this.createBid();
    },
    confirmBid() {
      // Logic for confirming bid
      this.createBid();
    },
    createBid() {
      // Example of how to send a POST request to create a bid
      const bidData = {
        projects: this.selectedProjects,
        bids: this.preview.map(item => ({ id: item.id, bidAmount: item.bidAmount }))
      };

      axios.post(`${this.backendUrl}/create_bid`, bidData)
        .then(response => {
          console.log('Bid created successfully:', response.data);
          // Optionally, you can reset the selectedProjects and preview arrays after successful bid creation
          this.selectedProjects = [];
          this.preview = null;
        })
        .catch(error => {
          console.error('Error creating bid:', error);
        });
    },
    formatDate(timestamp) {
      // Create a new Date object with the timestamp (in milliseconds)
      const date = new Date(timestamp);
      // Format the date to a human-readable format
      return date.toLocaleString();
    },
    formatHeader(header) {
      // Capitalize the first letter of each word after an underscore
      return header.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
  },
  computed: {
    // Compute rounded values for budget_minimum_usd and budget_maximum_usd
    roundedProjects() {
      return this.projects.map(project => ({
        ...project,
        budget_minimum_usd: parseFloat(project.budget_minimum_usd).toFixed(0), // Round to 2 decimal places
        budget_maximum_usd: parseFloat(project.budget_maximum_usd).toFixed(0), // Round to 2 decimal places
        submitdate: this.formatDate(project.submitdate), // Convert Unix timestamp to human-readable date
        bid_stats_bid_avg: parseFloat(project.bid_stats_bid_avg).toFixed(1), // Format to display only one digit after the decimal point
      }));
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
</style>
