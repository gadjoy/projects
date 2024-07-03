import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import DragAndDrop from '../components/DragAndDrop.vue';
import PdfViewWithChatbox from '../components/PdfViewWithChatbox.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/drag-and-drop',
    name: 'DragAndDrop',
    component: DragAndDrop
  },
  {
    path: '/pdf-view-chat',
    name: 'PdfViewWithChatbox',
    component: PdfViewWithChatbox
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
