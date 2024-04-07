<template>
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
</template>

<script>
import showdown from 'showdown';

export default {
  data() {
    return {
      showModal: false,
      modalDescription: '',
      showProposalModal: false,
      modalProposal: '',
      renderedProposal: '',
    };
  },
  methods: {
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
      this.renderedProposal = new showdown.Converter().makeHtml(proposal);
    },
    closeProposalModal() {
      this.showProposalModal = false;
      this.modalProposal = '';
      this.renderedProposal = '';
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    confirmBid(index) {
      this.$emit('confirmBid', index);
    },
  },
  props: {
    preview: {
      type: Array,
      required: true,
    },
    previewLoading: {
      type: Boolean,
      required: true,
    },
    selectedProjects: {
      type: Array,
      required: true,
    },
    projectHeaders: {
      type: Array,
      required: true,
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
</style>