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
            <th v-for="header in projectHeaders" :key="header" v-if="header !== 'proposal'">{{ formatHeader(header) }}</th>
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
            <td v-for="header in projectHeaders" :key="header" v-if="header !== 'proposal'">
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
          <div v-html="modalProposal"></div>
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

    <!-- Loading indicator for preview -->
    <div v-if="loadingPreview" class="loading-preview">
      Loading...
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import showdown from 'showdown';

export default {
  data() {
    return {
      query: '',
      projects: [],
      selectedProjects: [],
      loading: false,
      loadingPreview: false, // Added loading indicator for preview
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
        'proposal'
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
      this.modalProposal = proposal;
      this.showProposalModal = true;
    },
    closeProposalModal() {
      this.showProposalModal = false;
      this.modalProposal = '';
    },
    async previewBid() {
      if (this.selectedProjects.length === 0) {
        this.preview = [];
        return;
      }

      this.loadingPreview = true; // Show loading indicator
      this.preview = [];

      for (const projectId of this.selectedProjects) {
        const project = this.projects.find((p) => p.id === projectId);
        const previewItem = {};

        this.projectHeaders.forEach((header) => {
          previewItem[header] = project[header] || 'Not available';
        });

        previewItem.bidAmount = '';

        // Call generateAndShowProposal method for each selected project
        previewItem.proposal = await this.generateAndShowProposal(projectId);

        this.preview.push(previewItem);
      }

      this.loadingPreview = false; // Hide loading indicator
    },
    submitBid() {
      console.log('Submitting bids:', this.selectedProjects);
      this.createBid();
    },
    confirmBid() {
      this.createBid();
    },
    createBid() {
      const bidData = {
        projects: this.selectedProjects,
        bids: this.preview.map(item => ({ id: item.id, bidAmount: item.bidAmount }))
      };

      axios.post(`${this.backendUrl}/create_bid`, bidData)
        .then(response => {
          console.log('Bid created successfully:', response.data);
          this.selectedProjects = [];
          this.preview = null;
        })
        .catch(error => {
          console.error('Error creating bid:', error);
        });
    },
    async generateAndShowProposal(id) {
      try {
        const response = await axios.get(`${this.backendUrl}/generate_proposal`, {
          params: {
            project_id: id,
          },
        });

        // Convert Markdown proposal to HTML using Showdown
        const converter = new showdown.Converter();
        return converter.makeHtml(response.data.proposal || 'No proposal available');
      } catch (error) {
        console.error('Error fetching proposal:', error);
        return 'No proposal available';
      }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    formatHeader(header) {
      return header.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
  },
  computed: {
    roundedProjects() {
      return this.projects.map(project => ({
        ...project,
        budget_minimum_usd: parseFloat(project.budget_minimum_usd).toFixed(0),
        budget_maximum_usd: parseFloat(project.budget_maximum_usd).toFixed(0),
        submitdate: this.formatDate(project.submitdate),
        bid_stats_bid_avg: parseFloat(project.bid_stats_bid_avg).toFixed(1),
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

/* Loading indicator style */
.loading-preview {
  margin-top: 20px;
  font-style: italic;
}
</style>
