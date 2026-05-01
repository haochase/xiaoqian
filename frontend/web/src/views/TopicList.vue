<template>
  <div class="page-wrapper">
    <div class="topic-list">
      <div class="header">
        <h2>🌿 我的话题</h2>
        <button class="create-btn" @click="showCreate = true">
          <span>＋</span> 创建话题
        </button>
      </div>

      <div class="topic-cards" v-if="topics.length">
        <div
          v-for="t in topics"
          :key="t.id"
          class="topic-card"
        >
          <router-link :to="{ name: 'Chat', params: { sessionId: t.id } }" class="topic-link">
            <span class="topic-icon">{{ categoryIcon(t.category) }}</span>
            <div class="topic-info">
              <span class="topic-title">{{ t.title }}</span>
              <span class="topic-category">{{ categoryLabel(t.category) }}</span>
            </div>
            <span class="topic-arrow">→</span>
          </router-link>
        </div>
      </div>

      <div v-else class="empty-state">
        <span class="empty-icon">📝</span>
        <p>还没有话题，点击上方按钮创建一个吧</p>
      </div>

      <!-- Modal -->
      <div v-if="showCreate" class="modal" @click.self="showCreate = false">
        <div class="modal-content">
          <h3>✨ 新建话题</h3>
          <form @submit.prevent="createTopic">
            <div class="field">
              <label>标题</label>
              <input v-model="newTopic.title" required placeholder="例如：今日天气、猪肉价格..." />
            </div>
            <div class="field">
              <label>类别</label>
              <select v-model="newTopic.category" required>
                <option value="">选择类别</option>
                <option value="weather">🌤️ 天气</option>
                <option value="price">💰 价格</option>
                <option value="news">📰 新闻</option>
                <option value="celebrity">🌟 名人动态</option>
                <option value="custom">🎯 自定义</option>
              </select>
            </div>
            <div class="actions">
              <button type="submit" class="save-btn">保存</button>
              <button type="button" class="cancel-btn" @click="showCreate = false">取消</button>
            </div>
          </form>
        </div>
      </div>

      <router-link to="/dashboard" class="back-link">← 返回首页</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../store/auth';
import api from '../api';

interface Topic {
  id: string;
  title: string;
  category: string;
}

const auth = useAuthStore();
const topics = ref<Topic[]>([]);
const showCreate = ref(false);
const newTopic = ref({ title: '', category: '' });

const categoryIcon = (cat: string) => {
  const map: Record<string, string> = {
    weather: '🌤️', price: '💰', news: '📰', celebrity: '🌟'
  };
  return map[cat] || '🎯';
};

const categoryLabel = (cat: string) => {
  const map: Record<string, string> = {
    weather: '天气', price: '价格', news: '新闻', celebrity: '名人动态', custom: '自定义'
  };
  return map[cat] || cat;
};

const fetchTopics = async () => {
  const resp = await api.get('/topics');
  topics.value = resp.data;
};

const createTopic = async () => {
  await api.post('/topics', {
    title: newTopic.value.title,
    category: newTopic.value.category,
    is_active: true,
  });
  showCreate.value = false;
  newTopic.value = { title: '', category: '' };
  await fetchTopics();
};

onMounted(() => {
  if (auth.isAuthenticated()) fetchTopics();
});
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  padding-top: 4rem;
}

.topic-list {
  max-width: 640px;
  width: 100%;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(126, 200, 160, 0.12), 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #37474F;
}

.create-btn {
  padding: 0.5rem 1.2rem;
  background: linear-gradient(135deg, #66BB6A, #43A047);
  color: #fff;
  border: none;
  border-radius: 14px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 187, 106, 0.25);
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(102, 187, 106, 0.35);
}

.create-btn span {
  font-size: 1.1rem;
}

.topic-cards {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.topic-card {
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.topic-card:hover {
  transform: translateX(4px);
}

.topic-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  text-decoration: none;
  background: linear-gradient(135deg, #F5F5F5, #FAFAFA);
  border: 1px solid #E0E0E0;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.topic-link:hover {
  background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
  border-color: #A5D6A7;
}

.topic-icon {
  font-size: 1.8rem;
  flex-shrink: 0;
}

.topic-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.topic-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #37474F;
}

.topic-category {
  font-size: 0.8rem;
  color: #90A4AE;
}

.topic-arrow {
  font-size: 1.2rem;
  color: #B0BEC5;
  flex-shrink: 0;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #B0BEC5;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

/* Modal */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: #fff;
  padding: 2rem;
  border-radius: 20px;
  width: 360px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
}

.modal-content h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #37474F;
  margin-bottom: 1.25rem;
}

.field {
  margin-bottom: 1rem;
}

.field label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #546E7A;
}

.field input, .field select {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: inherit;
  outline: none;
  transition: all 0.3s ease;
}

.field input:focus, .field select:focus {
  border-color: #66BB6A;
  box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.1);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.save-btn {
  padding: 0.55rem 1.5rem;
  background: linear-gradient(135deg, #66BB6A, #43A047);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
}

.cancel-btn {
  padding: 0.55rem 1.5rem;
  background: #F5F5F5;
  color: #78909C;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
}

.back-link {
  display: inline-block;
  margin-top: 1.5rem;
  color: #90A4AE;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: #66BB6A;
}
</style>
