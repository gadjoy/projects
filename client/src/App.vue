<template>
  <div id="app" class="container mt-5">
    <h1 class="text-center mb-4">Resume Customization</h1>
    <p class="text-center mb-4">
      Easily customize your resume for any job. Just upload your resume and
      paste the job description below.
    </p>

    <div class="row">
      <!-- Upload Section -->
      <div class="col-md-6">
        <div class="card shadow-sm mb-4 uniform-card">
          <div class="card-body">
            <h5 class="card-title text-center">Upload Resume</h5>
            <div class="mb-4 input-group">
              <input
                type="file"
                class="form-control"
                @change="handleResumeUpload"
                accept=".pdf,.docx"
              />
              <button @click="submitFiles" class="btn btn-sm btn-custom">
                Upload
              </button>
            </div>
            <div class="resume-container">
              <textarea
                v-model="uploadedResumeText"
                class="form-control resume-text"
                readonly
                rows="3"
              ></textarea>
              <button
                @click="openModal('uploadedResume')"
                class="btn btn-sm btn-custom mt-2"
              >
                See More
              </button>
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
              <button
                @click="openModal('jobDescription')"
                class="btn btn-sm btn-custom mt-2"
              >
                See More
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Customized Resume Section -->
    <transition name="fade">
      <div
        v-if="customizedResume"
        class="w-100 mb-4"
        style="max-width: 1000px; margin: auto;"
      >
        <!-- Centered Download Button placed outside the card -->
        <div class="text-center mb-3">
          <button @click="downloadResumeAsWord" class="btn btn-sm btn-custom">
            Download
          </button>
        </div>

        <!-- Customized Resume Section -->
        <div class="card">
          <div class="card-body">
            <h5 class="card-title text-center">Customized Resume</h5>
            <div class="resume-container">
              <textarea
                v-model="formattedCustomizedResume"
                class="form-control resume-text"
                readonly
                rows="3"
              ></textarea>
              <button
                @click="openModal('customizedResume')"
                class="btn btn-sm btn-custom mt-2"
              >
                See More
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex flex-column align-items-center mt-5">
      <div
        class="spinner-border text-primary"
        role="status"
        style="width: 3rem; height: 3rem;"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
      <h5 class="mt-3 text-primary">
        Generating customized resume, please wait...
      </h5>
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
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";

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
  computed: {
    formattedCustomizedResume() {
      return this.customizedResume ? this.customizedResume.replace(/\*/g, '') : '';
    },
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
    downloadResumeAsWord() {
      if (!this.customizedResume) {
        alert('No customized resume available to download.');
        return;
      }

      const cleanedResume = this.customizedResume.replace(/\*/g, ''); // Remove asterisks

      const lines = cleanedResume.split("\n").map(line => line.trim()).filter(line => line !== "");
      const doc = new Document({
        sections: [
          {
            properties: {},
            children: lines.map((line) =>
              new Paragraph({
                children: [
                  new TextRun({
                    text: line,
                    break: 1, // Ensure line breaks are handled properly
                  }),
                ],
              })
            ),
          },
        ],
      });

      Packer.toBlob(doc).then((blob) => {
        saveAs(blob, "customized_resume.docx");
      }).catch((error) => {
        console.error('Error creating Word document:', error);
      });
    },
    openModal(type) {
      if (type === 'uploadedResume') {
        this.modalText = this.uploadedResumeText;
      } else if (type === 'jobDescription') {
        this.modalText = this.jobDescription;
      } else if (type === 'customizedResume') {
        this.modalText = this.formattedCustomizedResume; // Display formatted text in modal
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
  height: 93px;
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
