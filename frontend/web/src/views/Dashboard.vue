<template>
  <div class="dashboard">
    <h1>欢迎，{{ user?.nickname || '用户' }}</h1>
    <p>这里是小倩的后台管理面板，您可以查看话题、启动聊天等。</p>
    <router-link class="nav-btn" to="/topics">管理话题</router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '../store/auth';

const auth = useAuthStore();
const user = computed(() => auth.user);
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 80px auto;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
}
.nav-btn {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.8rem 1.5rem;
  background: #10b981;
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}
.nav-btn:hover { background: #059669; }
</style>
