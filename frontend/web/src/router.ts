import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Login from './views/Login.vue';
import Dashboard from './views/Dashboard.vue';
import TopicList from './views/TopicList.vue';
import Chat from './views/Chat.vue';

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/topics', name: 'TopicList', component: TopicList, meta: { requiresAuth: true } },
  { path: '/chat/:sessionId', name: 'Chat', component: Chat, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// navigation guard for auth
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
