import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Home from './views/Home.vue';
import Chat from './views/Chat.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'Home', component: Home },
  { path: '/chat/:sessionId', name: 'Chat', component: Chat },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
