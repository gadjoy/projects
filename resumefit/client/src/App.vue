<template>
  <div class="resume-fit container">
    <h1 class="text-center">RESUME FIT</h1>
    <p class="text-center text-muted">Customize your resume based on the job description</p>

    <div class="row upload-section">
      <div class="col-md-6">
        <h3 class="text-center">Base Resume</h3>
        <input type="file" @change="handleFileUpload" class="form-control mb-2" />
        <textarea
          v-model="baseResume"
          placeholder="Upload your existing resume"
          class="form-control"
          rows="10"
        ></textarea>
      </div>

      <div class="col-md-6">
        <h3 class="text-center">Job Description</h3>
        <textarea
          v-model="jobDescription"
          placeholder="Provide the job description for customization"
          class="form-control job-description-box"
        ></textarea>
      </div>
    </div>

    <div class="row customized-resume mt-4">
      <div class="col-12 text-center">
        <button
          @click="sendOutputToServer"
          :disabled="isProcessing"
          type="button"
          class="btn btn-success mb-3"
        >
          Customize
        </button>
        <button
          v-if="customizedResume"
          @click="downloadPDF"
          type="button"
          class="btn btn-primary mb-3 ml-2"
        >
          Download
        </button>
        <!-- Spinner -->
        <div v-if="isProcessing" class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <div class="col-12">
        <h3 class="text-center">Customized Resume</h3>
        <div v-html="renderedMarkdown" class="markdown-output"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as pdfjsLib from 'pdfjs-dist/webpack';
import { marked } from 'marked';
import mammoth from 'mammoth';
import html2pdf from 'html2pdf.js';

pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

// const api_server = 'http://localhost:5000'; // Local
// const api_server = 'https://projects-z23q.onrender.com'; // Render
const api_server = 'https://resume-fit-api-server-2504145397.asia-northeast1.run.app'; // Google Cloud Run

export default {
  data() {
    return {
      baseResume: '',
      jobDescription: '',
      customizedResume: '',
      isProcessing: false,
      processingInterval: null,
    };
  },
  computed: {
    renderedMarkdown() {
      return marked(this.customizedResume || '');
    },
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      const fileType = file.type;

      if (fileType === 'application/pdf') {
        this.readPdf(file);
      } else if (fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        this.readDocx(file);
      } else {
        alert('Please upload a PDF or DOCX file.');
      }
    },
    readPdf(file) {
      const reader = new FileReader();

      reader.onload = async (e) => {
        const pdfData = new Uint8Array(e.target.result);
        const pdf = await pdfjsLib.getDocument({ data: pdfData }).promise;
        let textContent = '';

        for (let i = 0; i < pdf.numPages; i++) {
          const page = await pdf.getPage(i + 1);
          const text = await page.getTextContent();
          text.items.forEach((item) => {
            textContent += item.str + ' ';
          });
        }

        this.baseResume = textContent.trim();
      };

      reader.readAsArrayBuffer(file);
    },
    readDocx(file) {
      const reader = new FileReader();

      reader.onload = async (e) => {
        const arrayBuffer = e.target.result;
        const { value } = await mammoth.extractRawText({ arrayBuffer });
        this.baseResume = value.trim();
      };

      reader.readAsArrayBuffer(file);
    },
    async sendOutputToServer() {
      if (!this.baseResume || !this.jobDescription) {
        alert('Please upload a base resume and enter a job description.');
        return;
      }

      this.isProcessing = true;

      try {
        const response = await axios.post(`${api_server}/input`, {
          base_resume: this.baseResume,
          job_description: this.jobDescription,
        });

        if (response.data.message === 'Resume processed successfully') {
          this.startPollingForCustomizedResume();
        }
      } catch (error) {
        alert('An error occurred while sending the resume.');
        console.error(error);
      } finally {
        this.isProcessing = false;
      }
    },
    startPollingForCustomizedResume() {
      this.processingInterval = setInterval(async () => {
        try {
          const result = await axios.get(`${api_server}/output`);
          if (result.data.customized_resume) {
            this.customizedResume = result.data.customized_resume;
            clearInterval(this.processingInterval);
            this.processingInterval = null;
          }
        } catch (error) {
          console.error('An error occurred while fetching the customized resume.', error);
        }
      }, 2000);
    },
    downloadPDF() {
      if (!this.customizedResume) {
        alert('No customized resume available to download.');
        return;
      }

      const element = document.createElement('div');
      element.style.padding = '30px'; // Add padding for margins
      // element.style.width = '595px'; // A4 width in points (595px)
      element.style.fontSize = '12px'; // Optional: set a base font size
      element.innerHTML = this.renderedMarkdown;

      const options = {
        filename: 'customized_resume.pdf',
        margin: 1, // Add a margin in inches
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'pt', format: 'a4', orientation: 'portrait' },
      };

      html2pdf().from(element).set(options).save();
    },
  },
};
</script>

<style scoped>
.resume-fit {
  margin-top: 20px;
}

textarea {
  width: 100%;
  height: 300px;
  resize: none;
}

.job-description-box {
  height: 345px; /* Set the height of the job description box to 345px */
}

.markdown-output {
  width: 100%;
  margin-top: 10px;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #f9f9f9;
  min-height: 300px;
}
</style>
