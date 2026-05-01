<template>
  <div id="app">
    <div v-if="!auth.ready" class="loading-screen">
      <span class="loader-icon">🌸</span>
      <p>加载中...</p>
    </div>
    <router-view v-else />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './store/auth';

const auth = useAuthStore();

onMounted(() => {
  auth.autoLogin();
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(160deg, #e8f5e9 0%, #e3f2fd 30%, #fce4ec 70%, #fff8e1 100%);
  background-attachment: fixed;
  min-height: 100vh;
}

#app { min-height: 100vh; }

.loading-screen {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #90A4AE;
  gap: 1rem;
}

.loader-icon {
  font-size: 3rem;
  animation: float 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
