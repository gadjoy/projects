import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';  // Add this line for Font Awesome

createApp(App).use(router).mount('#app');
