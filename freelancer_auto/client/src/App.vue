<template>
  <div>
    <h1>FREELANCER AUTO BIDDER</h1>
    <!-- Display tokens input if tokens are not submitted -->
    <div v-if="!tokensSubmitted">
      <h2>Enter Tokens</h2>
      <div>
        <label for="oauth_token">OAuth Token:</label>
        <input v-model="oauthToken" type="text" id="oauth_token" placeholder="Enter OAuth Token">
      </div>
      <div>
        <label for="api_key">API Key:</label>
        <input v-model="apiKey" type="text" id="api_key" placeholder="Enter API Key">
      </div>
      <button @click="submitTokens" :disabled="!oauthToken || !apiKey">Submit Tokens</button>
    </div>

    <!-- Display query input if tokens are submitted -->
    <div v-else>
      <label for="query">Query:</label>
      <input v-model="query" type="text" id="query" placeholder="Type your query here..." />
      <button @click="handleSearch" :disabled="!isQueryTyped || loading">Search</button>

      <!-- Message for empty query -->
      <p v-if="!isQueryTyped && searchClicked" style="color: red;">Please enter a query.</p>

      <!-- Spinner while loading projects -->
      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>

      <!-- Display projects -->
      <div v-if="!loading && roundedProjects.length > 0">
        <table>
          <!-- Table headers -->
          <thead>
            <tr>
              <th v-for="header in projectHeaders" :key="header">{{ formatHeader(header) }}</th>
              <th>Select</th> <!-- Move checkbox column to the last position -->
            </tr>
          </thead>
          <!-- Table body -->
          <tbody>
            <tr v-for="project in roundedProjects" :key="project.id">
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
              <!-- Checkbox for selection -->
              <td>
                <input type="checkbox" v-model="selectedProjects" :value="project.id" />
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Buttons for preview and submit -->
        <div>
          <button @click="previewBid" :disabled="selectedProjects.length === 0">Propose</button>
          <button @click="previousPage" :disabled="nextOffset === 0">Previous</button>
          <button @click="nextPage" :disabled="!isQueryTyped || loading">Next</button>
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
            <!-- Use Showdown to render proposal in proper format -->
            <div class="proposal-content" v-html="renderedProposal"></div>
          </div>
        </div>

        <!-- Display Preview -->
        <div v-if="preview !== null" class="preview-container">
          <h2>Preview:</h2>
          <div v-if="previewLoading" class="spinner-container">
            <div class="spinner"></div>
          </div>
          <table v-else-if="selectedProjects.length > 0" class="preview-table">
            <!-- Table headers -->
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
                <th>Confirm</th> <!-- New column for confirm button -->
              </tr>
            </thead>
            <!-- Table body -->
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
                <!-- Dynamically set colspan to the number of columns minus 14 -->
                <td :colspan="projectHeaders.length - 14">
                  <input class="bid-input" type="number" v-model="item.bidAmount" placeholder="Enter bid amount">
                </td>
                <td>
                  <button @click="confirmBid(index)" :disabled="!item.bidAmount">Confirm</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else>No projects selected for preview.</p>
        </div>

      </div>
    </div>

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
<!-- Page to Display Versions -->
<AboutPage v-if="showVersions && !showAboutModal" class="versions">
  <span>{{ backendVersion }}</span>
  <span>{{ backendModifiedDate }}</span>
  <span>{{ frontendVersion }}</span>
  <span>{{ frontendModifiedDate }}</span>
  <span>{{ buildNumber }}</span>
  <span>{{ backendUrl }}</span>
</AboutPage>
  </div>
</template>

<script>
import axios from 'axios';
import showdown from 'showdown';
import AboutModal from './AboutModal.vue';

export default {
  components: {
    AboutModal,
  },
  data() {
    return {
      query: '',
      projects: [],
      selectedProjects: [],
      loading: false,
      // backendUrl: 'https://freelancer-auto-backend-rqvi.onrender.com',
      backendUrl: 'http://127.0.0.1:5000',
      preview: null,
      previewLoading: false,
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
      modalProposal: '',
      renderedProposal: '',
      searchClicked: false,
      backendVersion: '',
      backendModifiedDate: '',
      frontendVersion: 'v1.0.0',
      frontendModifiedDate: '01-04-2024',
      buildNumber: '001',
      showAboutModal: false,
      showVersions: false,
      nextOffset: 0, // Track offset for pagination
      oauthToken: '', // Added OAuth Token data property
      apiKey: '', // Added API Key data property
      tokensSubmitted: false, // Flag to track if tokens are submitted
    };
  },
  methods: {
    async submitTokens() {
      try {
        const response = await axios.post(`${this.backendUrl}/set_tokens`, {
          oauth_token: this.oauthToken,
          api_key: this.apiKey,
        });
        console.log(response.data.message);
        // Optionally, you can clear the input fields after successful submission
        this.oauthToken = '';
        this.apiKey = '';
        // Set tokensSubmitted to true after successful submission
        this.tokensSubmitted = true;
      } catch (error) {
        console.error('Error submitting tokens:', error);
      }
    },
    async handleSearch() {
      // Reset nextOffset when performing a new search
      this.nextOffset = 0;
      // Set searchClicked to true when search button is clicked
      this.searchClicked = true;

      // If query is empty, return and show the message
      if (!this.isQueryTyped) {
        return;
      }

      // If query is not empty, proceed with fetching projects
      this.fetchProjects();
    },
    async fetchProjects() {
  try {
    this.loading = true;
    // Clear the projects array before fetching new projects
    this.projects = [];
    const response = await axios.get(`${this.backendUrl}/search_projects`, {
      params: {
        query: this.query,
        offset: this.nextOffset, // Pass the nextOffset as a parameter
      },
    });

    // Concatenate new projects to existing projects array
    this.projects = this.projects.concat(response.data); // Use concat() to add new projects to existing ones

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
      // Convert Markdown proposal to HTML using Showdown
      this.renderedProposal = new showdown.Converter().makeHtml(proposal);
    },
    closeProposalModal() {
      this.showProposalModal = false;
      this.modalProposal = '';
      this.renderedProposal = '';
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

      // Set preview loading state to true to show spinner
      this.previewLoading = true;

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

      // Set preview loading state back to false after preview is complete
      this.previewLoading = false;
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

      axios.post(`${this.backendUrl}/place_bid`, bidData)
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
      let formattedHeader = header.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

      // Check if the header contains 'Usd' and replace it with 'USD'
      formattedHeader = formattedHeader.replace('Usd', 'USD');

      return formattedHeader;
    },
    nextPage() {
  // Increment nextOffset to fetch the next set of projects
  console.log('Current nextOffset:', this.nextOffset);
  this.nextOffset += 10; // Increment by 10 to fetch the next page
  console.log('Updated nextOffset:', this.nextOffset);
  // Fetch projects with the updated offset
  this.fetchProjects();
},

    previousPage() {
      // Ensure nextOffset doesn't go below 0
      this.nextOffset = Math.max(0, this.nextOffset - 10);
      // Fetch projects with the updated offset
      this.fetchProjects();
    },    
    
    showAbout() {
      this.showAboutModal = true;
      this.showVersions = true;
      this.fetchBackendVersion();
      this.fetchFrontendModifiedDate();
    },
    hideAbout() {
      this.showAboutModal = false;
      this.showVersions = false;
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
    fetchFrontendModifiedDate() {
      this.frontendModifiedDate = '01-04-2024';
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
    isQueryTyped() {
      return this.query.trim().length > 0; // Check if query is typed (ignores leading/trailing whitespace)
    },
    // Check if bid amount is entered for all selected projects
    canConfirmBid() {
      return this.preview.every(item => item.bidAmount !== '');
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

/* CSS for Bid Amount input field */
.bid-input {
  width: 100%; /* Ensure the input field fills the entire cell */
  box-sizing: border-box; /* Include padding and border in the width */
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
  overflow-x: auto;
}

/* Preview table style */
.preview-table {
  width: 100%;
  table-layout: auto; /* Allow table to adjust layout based on content */
  border-collapse: collapse;
  margin-top: 20px;
}

.preview-table th,
.preview-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  word-wrap: break-word; /* Wrap long words */
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
  table-layout: auto; /* Allow table to adjust layout based on content */
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

/* Proposal content style */
.proposal-content {
  text-align: left;
}
/* Style for disabled search button */
button:disabled {
  background-color: #ccc; /* Change background color */
  color: #666; /* Change text color */
  cursor: not-allowed; /* Change cursor to indicate it's not clickable */
}

button:disabled:hover {
  background-color: #ccc; /* Change background color on hover */
  color: #666; /* Change text color on hover */
}

/* Info button style */
.info-button {
  position: absolute; /* Position it relative to the nearest positioned ancestor */
  top: 20px; /* Adjust top position */
  right: 20px; /* Adjust right position */
  cursor: pointer;
  color: #3498db;
  z-index: 999; /* Ensure it's above other content */
}

.info-button i {
  font-size: 24px;
}

/* Versions display style */
.versions {
  position: fixed;
  top: 20px;
  right: 20px;
}

.versions span {
  display: block;
  margin-bottom: 5px;
}
</style>
