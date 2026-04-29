<template>
  <div class="chat-container">
    <h2>聊天会话</h2>
    <div class="messages" ref="msgContainer">
      <div v-for="msg in messages" :key="msg.id" :class="['msg', msg.role]">
        <span class="content">{{ msg.content }}</span>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="input-bar">
      <input v-model="input" placeholder="输入消息..." required />
      <button type="submit" class="send-btn">发送</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../store/auth';
import api from '../api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const route = useRoute();
const sessionId = route.params.sessionId as string;
const auth = useAuthStore();
const messages = ref<Message[]>([]);
const input = ref('');
let ws: WebSocket | null = null;
const msgContainer = ref<HTMLElement | null>(null);

const fetchHistory = async () => {
  const resp = await api.get(`/sessions/${sessionId}/messages`);
  messages.value = resp.data;
};

const initWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${sessionId}`);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.value.push({ id: data.id, role: data.role, content: data.content });
    scrollToBottom();
  };
  ws.onopen = () => console.log('WebSocket 已连接');
  ws.onclose = () => console.log('WebSocket 已关闭');
};

const sendMessage = () => {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  const payload = { role: 'user', content: input.value };
  ws.send(JSON.stringify(payload));
  messages.value.push({ id: Date.now().toString(), role: 'user', content: input.value });
  input.value = '';
  scrollToBottom();
};

const scrollToBottom = () => {
  setTimeout(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight;
    }
  }, 50);
};

onMounted(() => {
  if (auth.isAuthenticated()) {
    fetchHistory();
    initWebSocket();
  }
});

onBeforeUnmount(() => {
  if (ws) ws.close();
});
</script>

<style scoped>
.chat-container { max-width: 800px; margin: 80px auto; padding: 2rem; background: rgba(255,255,255,0.95); border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); display: flex; flex-direction: column; height: 80vh; }
.messages { flex: 1; overflow-y: auto; margin-bottom: 1rem; }
.msg { margin: 0.5rem 0; padding: 0.6rem 1rem; border-radius: 8px; max-width: 70%; }
.msg.user { background: #6366f1; color: #fff; align-self: flex-end; }
.msg.assistant { background: #e5e7eb; color: #111; align-self: flex-start; }
.input-bar { display: flex; }
.input-bar input { flex: 1; padding: 0.6rem; border: 1px solid #d1d5db; border-radius: 6px 0 0 6px; }
.send-btn { padding: 0.6rem 1rem; background: #10b981; color: #fff; border: none; border-radius: 0 6px 6px 0; cursor: pointer; }
</style>
