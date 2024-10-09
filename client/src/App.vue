<template>
  <div id="app" class="container mt-5">
    <h1 class="text-center mb-4">Resume Customization</h1>
    <p class="text-center mb-4">Easily customize your resume for any job. Just upload your resume and paste the job description below.</p>

    <div class="row">
      <!-- Upload Section -->
      <div class="col-md-6">
        <div class="card shadow-sm mb-4 uniform-card">
          <div class="card-body">
            <h5 class="card-title text-center">Upload Resume</h5>
            <div class="mb-4 input-group">
              <input type="file" class="form-control" @change="handleResumeUpload" accept=".pdf,.docx" />
              <button @click="submitFiles" class="btn btn-sm btn-custom">Upload</button>
            </div>
            <div class="resume-container">
              <h6>Uploaded Resume:</h6>
              <textarea
                v-model="uploadedResumeText"
                class="form-control resume-text"
                readonly
                rows="3"
              ></textarea>
              <button @click="openModal('uploadedResume')" class="btn btn-sm btn-custom mt-2">See More</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Description Section -->
      <div class="col-md-6">
        <div class="card shadow-sm mb-4 uniform-card">
          <div class="card-body">
            <h5 class="card-title text-center">Job Description</h5>
            <div class="resume-container">
              <textarea
                v-model="jobDescription"
                class="form-control job-description"
                placeholder="Paste the job description here..."
                rows="3"
              ></textarea>
              <button @click="openModal('jobDescription')" class="btn btn-sm btn-custom mt-2">See More</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Customized Resume Section -->
    <transition name="fade">
      <div v-if="customizedResume" class="card w-100 mb-4" style="max-width: 1000px; margin: auto;">
        <div class="card-body">
          <h5 class="card-title text-center">Customized Resume</h5>
          <div class="resume-container">
            <textarea
              v-model="customizedResume"
              class="form-control resume-text"
              readonly
              rows="3"
            ></textarea>
            <button @click="openModal('customizedResume')" class="btn btn-sm btn-custom mt-2">See More</button>
          </div>
          <div class="text-center mt-3">
            <button @click="downloadResume" class="btn btn-sm btn-custom">Download</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex flex-column align-items-center mt-5">
      <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5 class="mt-3 text-primary">Generating customized resume, please wait...</h5>
    </div>

    <!-- Modal for Reviewing Content -->
    <div v-if="modalVisible" class="modal-overlay">
      <div class="modal-content">
        <h5 class="text-center">Review Content</h5>
        <textarea
          v-model="modalText"
          class="form-control modal-textarea"
          readonly
        ></textarea>
        <div class="text-center mt-3">
          <button @click="closeModal" class="btn btn-sm btn-custom">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from "jspdf";

export default {
  data() {
    return {
      resumeFile: null,
      jobDescription: '',
      customizedResume: null,
      uploadedResumeText: '',
      loading: false,
      modalVisible: false,
      modalText: '',
      backendUrl: 'https://resume-fit-4.onrender.com',
    };
  },
  methods: {
    handleResumeUpload(event) {
      this.resumeFile = event.target.files[0];
    },
    async submitFiles() {
      if (!this.resumeFile || !this.jobDescription) {
        alert('Please upload your resume and enter the job description.');
        return;
      }

      this.loading = true;

      try {
        const resumeFormData = new FormData();
        resumeFormData.append('file', this.resumeFile);
        const resumeResponse = await fetch(`${this.backendUrl}/upload_resume`, {
          method: 'POST',
          body: resumeFormData,
        });
        const resumeData = await resumeResponse.json();
        if (!resumeResponse.ok) {
          alert('Error uploading resume: ' + resumeData.error);
          return;
        }

        this.uploadedResumeText = resumeData.resume_text; // Store uploaded resume text

        const requestBody = {
          resume_text: this.uploadedResumeText,
          job_description: this.jobDescription,
        };
        const customizationResponse = await fetch(`${this.backendUrl}/generate_customized_resume`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
        const customizationData = await customizationResponse.json();
        if (!customizationResponse.ok) {
          alert('Error generating customized resume: ' + customizationData.error);
          return;
        }

        this.customizedResume = customizationData.customized_resume;
      } catch (error) {
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    },
    downloadResume() {
      const doc = new jsPDF('p', 'mm', 'a4'); // Portrait orientation, millimeters, A4 size

      // Start with a base font size
      let fontSize = 10;
      doc.setFontSize(fontSize); // Set initial font size
      const title = "Customized Resume";
      const titleHeight = 10;

      // Add title to the first page
      doc.text(title, 10, titleHeight);
      let y = titleHeight + 20; // Start placing text below the title

      // Split content into lines for better placement
      const lines = doc.splitTextToSize(this.customizedResume, 190); // 190mm width for A4

      const maxLinesPerPage = Math.floor(297 / fontSize) - 2; // Max lines per page (A4 height - margins / line height)
      const totalPages = Math.ceil(lines.length / maxLinesPerPage); // Calculate total pages needed

      // Adjust font size if total pages exceed 2
      if (totalPages > 2) {
        fontSize = 8; // Reduce font size
        doc.setFontSize(fontSize);
      }

      // Recalculate max lines per page with the new font size
      const adjustedMaxLinesPerPage = Math.floor(297 / fontSize) - 2;
      const adjustedContentLines = lines.slice(0, adjustedMaxLinesPerPage * 2); // Get only the lines that fit within 2 pages

      adjustedContentLines.forEach((line) => {
        // Check if we need to add a new page
        if (y > 297 - 10) { // Check if we need to add a new page before adding the next line
          doc.addPage();
          y = titleHeight + 20; // Reset y position for new page
          doc.setFontSize(fontSize); // Reset font size if it was changed
        }

        // Check for the words "Customized" and "Resume" to set them as bold
        const wordsToBold = ['Customized', 'Resume'];
        const parts = line.split(new RegExp(`(${wordsToBold.join('|')})`, 'g'));

        parts.forEach((part) => {
          if (wordsToBold.includes(part)) {
            doc.setFont("Helvetica", "bold"); // Set to bold font
          } else {
            doc.setFont("Helvetica", "normal"); // Set to normal font
          }
          doc.text(part, 10, y);
          y += fontSize; // Increase y position by the font size
        });
      });

      // Save the PDF
      doc.save('customized_resume.pdf');
    },
    openModal(type) {
      if (type === 'uploadedResume') {
        this.modalText = this.uploadedResumeText;
      } else if (type === 'jobDescription') {
        this.modalText = this.jobDescription;
      } else if (type === 'customizedResume') {
        this.modalText = this.customizedResume;
      }
      this.modalVisible = true;
    },
    closeModal() {
      this.modalVisible = false;
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
}

.uniform-card {
  border: 1px solid #ccc;
}

.card {
  background-color: #ffffff;
  border-radius: 10px;
}

.resume-container {
  position: relative;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin-top: 10px;
}

.resume-text {
  height: 65px;
}

.job-description {
  height: 150px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
}

.modal-textarea {
  height: 500px;
}

.btn-custom {
  background-color: #007bff;
  color: white;
}

.btn-custom:hover {
  background-color: #0056b3;
}
</style>
