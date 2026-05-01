<template>
  <div class="page-wrapper">
    <div class="dashboard">
      <span class="greeting-emoji">🌟</span>
      <h1>你好呀，{{ user?.nickname || '朋友' }}</h1>
      <p class="desc">今天想聊点什么呢？小倩随时在线陪你~</p>

      <div class="quick-cards">
        <router-link to="/topics" class="quick-card card-green">
          <span class="card-icon">📋</span>
          <span class="card-label">管理话题</span>
          <span class="card-desc">定制你的聊天兴趣</span>
        </router-link>
        <div class="quick-card card-blue" @click="() => {}">
          <span class="card-icon">💬</span>
          <span class="card-label">开始聊天</span>
          <span class="card-desc">选择一个话题开始</span>
        </div>
      </div>

      <div class="status-bar">
        <div class="status-dot"></div>
        <span>小倩在线中 · 随时为你服务</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '../store/auth';

const auth = useAuthStore();
const user = computed(() => auth.user);
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.dashboard {
  max-width: 600px;
  width: 100%;
  padding: 3rem 2.5rem;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(126, 200, 160, 0.12), 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.6);
  text-align: center;
}

.greeting-emoji {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.5rem;
  animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(10deg); }
  75% { transform: rotate(-10deg); }
}

h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #37474F;
  margin-bottom: 0.5rem;
}

.desc {
  font-size: 1rem;
  color: #90A4AE;
  margin-bottom: 2rem;
}

.quick-cards {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.quick-card {
  flex: 1;
  padding: 1.5rem 1rem;
  border-radius: 18px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

.card-green {
  background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
  border: 1px solid #A5D6A7;
}

.card-green:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(102, 187, 106, 0.2);
}

.card-blue {
  background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
  border: 1px solid #90CAF9;
}

.card-blue:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(66, 165, 245, 0.2);
}

.card-icon {
  font-size: 2rem;
}

.card-label {
  font-size: 1rem;
  font-weight: 600;
  color: #37474F;
}

.card-desc {
  font-size: 0.8rem;
  color: #78909C;
}

.status-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #F1F8E9;
  border-radius: 20px;
  font-size: 0.85rem;
  color: #689F38;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #66BB6A;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.3); }
}
</style>
