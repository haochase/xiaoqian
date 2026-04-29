<template>
  <div class="topic-list">
    <h2>我的话题</h2>
    <button class="btn" @click="showCreate = true">+ 创建话题</button>
    <ul v-if="topics.length" class="list">
      <li v-for="t in topics" :key="t.id" class="list-item">
        <router-link :to="{ name: 'Chat', params: { sessionId: t.id } }">
          {{ t.title }}
        </router-link>
        <span class="category">{{ t.category }}</span>
      </li>
    </ul>
    <p v-else>暂无话题，快去创建吧。</p>

    <!-- 创建话题弹窗 -->
    <div v-if="showCreate" class="modal">
      <div class="modal-content">
        <h3>新建话题</h3>
        <form @submit.prevent="createTopic">
          <div class="field">
            <label>标题</label>
            <input v-model="newTopic.title" required />
          </div>
          <div class="field">
            <label>类别</label>
            <input v-model="newTopic.category" required />
          </div>
          <div class="actions">
            <button type="submit" class="btn">保存</button>
            <button type="button" class="btn cancel" @click="showCreate = false">取消</button>
          </div>
        </form>
      </div>
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
  if (auth.isAuthenticated()) {
    fetchTopics();
  } else {
    // redirect handled by router guard
  }
});
</script>

<style scoped>
.topic-list { max-width: 800px; margin: 80px auto; padding: 2rem; background: rgba(255,255,255,0.95); border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.btn { margin: 1rem 0; padding: 0.6rem 1.2rem; background: #6366f1; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.list { list-style: none; padding: 0; }
.list-item { padding: 0.8rem 0; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }
.category { font-size: 0.9rem; color: #6b7280; }
/* Modal */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; }
.modal-content { background: #fff; padding: 2rem; border-radius: 12px; width: 320px; }
.field { margin-bottom: 1rem; }
.actions { display: flex; justify-content: flex-end; gap: 0.5rem; }
.cancel { background: #d1d5db; }
</style>
