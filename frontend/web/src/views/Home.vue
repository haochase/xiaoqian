<template>
  <div class="home">
    <header class="hero">
      <span class="hero-emoji">🌸</span>
      <h1>小倩 · 兴趣聊天助手</h1>
      <p>选一个你感兴趣的话题，开始聊天吧</p>
    </header>

    <div class="grid">
      <section
        v-for="cat in categories"
        :key="cat.key"
        class="category-section"
        :style="{ '--cat-color': cat.color, '--cat-bg': cat.bg, '--cat-border': cat.border }"
      >
        <h2 class="cat-title">
          <span class="cat-icon">{{ cat.icon }}</span>
          {{ cat.name }}
        </h2>
        <div class="topic-cards">
          <button
            v-for="topic in cat.topics"
            :key="topic.id"
            class="topic-card"
            @click="openTopic(topic)"
            :disabled="topic.loading"
          >
            <span class="topic-emoji">{{ topic.icon }}</span>
            <span class="topic-name">{{ topic.name }}</span>
            <span v-if="topic.loading" class="topic-spinner">⏳</span>
            <span v-else class="topic-arrow">→</span>
          </button>
        </div>
      </section>
    </div>

    <footer class="footer">
      <p>小倩 · 主动式兴趣聊天助手 · Powered by AI</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import api from '../api';

const router = useRouter();
const auth = useAuthStore();

interface TopicDef {
  id: string;
  name: string;
  icon: string;
  category: string;
  loading: boolean;
}

interface CategoryDef {
  key: string;
  name: string;
  icon: string;
  color: string;
  bg: string;
  border: string;
  topics: TopicDef[];
}

const categories = ref<CategoryDef[]>([
  {
    key: 'sports', name: '体育新闻', icon: '⚽',
    color: '#2E7D32', bg: 'linear-gradient(135deg, #E8F5E9, #C8E6C9)', border: '#A5D6A7',
    topics: [
      { id: 's1', name: '足球热点', icon: '⚽', category: 'news', loading: false },
      { id: 's2', name: '篮球热点', icon: '🏀', category: 'news', loading: false },
      { id: 's3', name: 'F1 赛车', icon: '🏎️', category: 'news', loading: false },
      { id: 's4', name: '自行车赛', icon: '🚴', category: 'news', loading: false },
      { id: 's5', name: '网球动态', icon: '🎾', category: 'news', loading: false },
    ]
  },
  {
    key: 'tech', name: '科技新闻', icon: '💻',
    color: '#1565C0', bg: 'linear-gradient(135deg, #E3F2FD, #BBDEFB)', border: '#90CAF9',
    topics: [
      { id: 't1', name: 'AI 人工智能', icon: '🤖', category: 'news', loading: false },
      { id: 't2', name: '手机数码', icon: '📱', category: 'news', loading: false },
      { id: 't3', name: '互联网动态', icon: '🌐', category: 'news', loading: false },
      { id: 't4', name: '太空探索', icon: '🚀', category: 'news', loading: false },
    ]
  },
  {
    key: 'finance', name: '金融财经', icon: '💰',
    color: '#E65100', bg: 'linear-gradient(135deg, #FFF8E1, #FFECB3)', border: '#FFD54F',
    topics: [
      { id: 'f1', name: 'A 股行情', icon: '📈', category: 'price', loading: false },
      { id: 'f2', name: '美股动态', icon: '🇺🇸', category: 'price', loading: false },
      { id: 'f3', name: '加密货币', icon: '🪙', category: 'price', loading: false },
      { id: 'f4', name: '基金理财', icon: '💎', category: 'price', loading: false },
    ]
  },
  {
    key: 'world', name: '国际局势', icon: '🌍',
    color: '#6A1B9A', bg: 'linear-gradient(135deg, #F3E5F5, #E1BEE7)', border: '#CE93D8',
    topics: [
      { id: 'w1', name: '中美关系', icon: '🤝', category: 'news', loading: false },
      { id: 'w2', name: '欧洲动态', icon: '🏰', category: 'news', loading: false },
      { id: 'w3', name: '中东局势', icon: '🕌', category: 'news', loading: false },
      { id: 'w4', name: '亚太地区', icon: '🗾', category: 'news', loading: false },
    ]
  },
  {
    key: 'travel', name: '旅游演出', icon: '🎭',
    color: '#AD1457', bg: 'linear-gradient(135deg, #FCE4EC, #F8BBD0)', border: '#F48FB1',
    topics: [
      { id: 'tr1', name: '热门旅游', icon: '✈️', category: 'custom', loading: false },
      { id: 'tr2', name: '演唱会', icon: '🎵', category: 'custom', loading: false },
      { id: 'tr3', name: '展览推荐', icon: '🎨', category: 'custom', loading: false },
      { id: 'tr4', name: '美食探店', icon: '🍜', category: 'custom', loading: false },
    ]
  },
  {
    key: 'weather', name: '天气穿搭', icon: '🌤️',
    color: '#00695C', bg: 'linear-gradient(135deg, #E0F2F1, #B2DFDB)', border: '#80CBC4',
    topics: [
      { id: 'we1', name: '今日天气', icon: '☀️', category: 'weather', loading: false },
      { id: 'we2', name: '穿搭推荐', icon: '👗', category: 'custom', loading: false },
      { id: 'we3', name: '空气质量', icon: '🍃', category: 'weather', loading: false },
      { id: 'we4', name: '出行建议', icon: '🚗', category: 'weather', loading: false },
    ]
  },
  {
    key: 'celebrity', name: '明星热点', icon: '🌟',
    color: '#BF360C', bg: 'linear-gradient(135deg, #FFF3E0, #FFCCBC)', border: '#FFAB91',
    topics: [
      { id: 'c1', name: '娱乐圈', icon: '🎬', category: 'celebrity', loading: false },
      { id: 'c2', name: '影视推荐', icon: '🎥', category: 'celebrity', loading: false },
      { id: 'c3', name: '综艺热点', icon: '📺', category: 'celebrity', loading: false },
      { id: 'c4', name: '网红动态', icon: '📱', category: 'celebrity', loading: false },
    ]
  },
]);

const openTopic = async (topic: TopicDef) => {
  if (!auth.isAuthenticated()) return;
  topic.loading = true;
  try {
    const resp = await api.post('/topics', {
      title: topic.name,
      category: topic.category,
      is_active: true,
    });
    const topicId = resp.data.id;
    router.push({ name: 'Chat', params: { sessionId: topicId } });
  } catch (e) {
    console.error('创建话题失败', e);
  } finally {
    topic.loading = false;
  }
};
</script>

<style scoped>
.home {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

.hero {
  text-align: center;
  padding: 3rem 1rem 2rem;
}

.hero-emoji {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.hero h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #66BB6A, #42A5F5, #AB47BC);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.hero p {
  font-size: 1.05rem;
  color: #90A4AE;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.category-section {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.3s;
}

.category-section:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.cat-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--cat-color);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cat-icon {
  font-size: 1.4rem;
}

.topic-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
}

.topic-card {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.85rem 1rem;
  background: var(--cat-bg);
  border: 1.5px solid var(--cat-border);
  border-radius: 16px;
  font-size: 0.95rem;
  font-family: inherit;
  color: #37474F;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.topic-card:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.topic-card:active:not(:disabled) {
  transform: translateY(0);
}

.topic-card:disabled {
  opacity: 0.6;
  cursor: wait;
}

.topic-emoji {
  font-size: 1.3rem;
  flex-shrink: 0;
}

.topic-name {
  flex: 1;
  font-weight: 500;
}

.topic-arrow {
  color: var(--cat-color);
  font-weight: 700;
  font-size: 0.9rem;
  opacity: 0.5;
  transition: opacity 0.3s;
}

.topic-card:hover .topic-arrow {
  opacity: 1;
}

.topic-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.footer {
  text-align: center;
  margin-top: 3rem;
  color: #B0BEC5;
  font-size: 0.85rem;
}
</style>
