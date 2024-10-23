<template>
    <div class="container">
      <h1>AutoReach Content Generator</h1>
  
      <!-- User input for prompt -->
      <div class="input-section">
        <label for="userPrompt">Enter your prompt:</label>
        <textarea v-model="userPrompt" id="userPrompt" class="input-textarea"></textarea>
        <button @click="fetchGeneratedContent" class="btn">Generate Content</button>
      </div>
  
      <!-- Display formatted generated content -->
      <div v-if="generatedContent.instagramTwitter" class="content-section">
        <h2><b>Generated Instagram and Twitter Content</b></h2>
        <div v-html="formatGeneratedContent(generatedContent.instagramTwitter)"></div>
      </div>
      
      <div v-if="generatedContent.adCampaign" class="content-section">
        <h2><b>Generated Ad Campaign</b></h2>
        <div v-html="formatGeneratedContent(generatedContent.adCampaign)"></div>
      </div>
  
      <!-- Schedule post section -->
      <div class="schedule-section">
        <label for="scheduledTime">Schedule Time:</label>
        <input type="datetime-local" v-model="scheduledTime" id="scheduledTime" class="input-datetime" />
        <button @click="schedulePost" class="btn">Schedule Post</button>
      </div>
  
      <!-- Display scheduled posts in a table -->
      <div class="scheduled-posts-section">
        <h2><b>Scheduled Posts</b></h2>
        <table class="styled-table">
          <thead>
            <tr>
              <th>Content</th>
              <th>Scheduled Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="post in scheduledPosts" :key="post.scheduled_time">
              <td v-html="post.content"></td> <!-- Display only the content and hashtags -->
              <td>{{ post.scheduled_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        userPrompt: '',  // Input prompt for generating content
        generatedContent: {
          instagramTwitter: '', // Generated Instagram & Twitter content
          adCampaign: '' // Generated ad campaign content
        },
        scheduledTime: '',  // User-selected time for scheduling post
        scheduledPosts: []  // List of scheduled posts
      };
    },
    methods: {
      // Fetch generated content from the backend
      fetchGeneratedContent() {
        if (!this.userPrompt) {
          alert('Please enter a prompt.');
          return;
        }
  
        axios.post('http://127.0.0.1:5001/generate_content', { prompt: this.userPrompt })
          .then(response => {
            this.generatedContent.instagramTwitter = response.data.instagram_twitter_content;
            this.generatedContent.adCampaign = response.data.ad_campaign_content;
          })
          .catch(error => {
            console.error("Error generating content:", error);
          });
      },
  
      // Schedule the generated content automatically
      schedulePost() {
        if (!this.scheduledTime) {
          alert("Please select a date and time for scheduling.");
          return;
        }
  
        // Prepare content for the scheduled post
        const scheduledContent = this.generatedContent.instagramTwitter; // Use Instagram and Twitter content
  
        axios.post('http://127.0.0.1:5001/schedule_post', {
          content: scheduledContent,  // Auto-schedule the generated content
          scheduled_time: this.scheduledTime
        })
        .then(response => {
          alert(response.data.message);
          // Only keep the latest scheduled post with content and hashtags
          this.scheduledPosts = [{ content: scheduledContent, scheduled_time: this.scheduledTime }];
        })
        .catch(error => {
          console.error("Error scheduling post:", error);
        });
      },
  
      // Format generated content for display
      formatGeneratedContent(content) {
        return content
          .replace(/\n/g, '<br />') // Convert newlines to <br> tags
          .replace(/(^|\s)(#[a-zA-Z0-9_]+)/g, '$1<span style="color:blue;">$2</span>'); // Style hashtags
      }
    },
    mounted() {
      // this.fetchScheduledPosts();  // Uncomment if needed
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    font-size: 26px;
    color: #333;
    text-align: center;
  }
  
  h2 {
    font-size: 22px;
    margin-top: 20px;
    color: #444;
  }
  
  .input-section, .schedule-section, .content-section, .scheduled-posts-section {
    margin-top: 20px;
    padding: 15px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
  }
  
  .input-textarea {
    width: 100%;
    height: 100px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
    font-size: 16px;
  }
  
  .input-datetime {
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 8px;
    font-size: 16px;
  }
  
  .btn {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    font-size: 16px;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  .styled-table {
    margin-top: 20px;
    border-collapse: collapse;
    width: 100%;
  }
  
  .styled-table th, .styled-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
  }
  
  .styled-table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }
  
  .styled-table tbody tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .styled-table tbody tr:hover {
    background-color: #f1f1f1;
  }
  </style>