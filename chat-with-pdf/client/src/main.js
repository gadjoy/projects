import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import 'bootstrap/dist/css/bootstrap.min.css';  // Add this line for Bootstrap
import '@fortawesome/fontawesome-free/css/all.css';  // Add this line for Font Awesome

import 'bootstrap';  // Add this line for Bootstrap

createApp(App).use(router).mount('#app');