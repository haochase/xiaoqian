<template>
  <div class="chat-page">
    <div class="chat-container">
      <div class="chat-header">
        <router-link to="/" class="back-btn">← 首页</router-link>
        <span class="header-title">💬 聊天中</span>
        <span class="online-dot"></span>
      </div>

      <div class="messages" ref="msgContainer">
        <div v-if="messages.length === 0 && !isTyping" class="empty-chat">
          <span class="empty-emoji">🌸</span>
          <p>在下方输入消息，和我聊天吧~</p>
        </div>
        <div v-for="msg in messages" :key="msg.id" :class="['msg', msg.role]">
          <div class="msg-bubble">
            <span class="msg-content">{{ msg.content }}</span>
          </div>
        </div>
        <div v-if="isTyping" class="msg assistant">
          <div class="msg-bubble typing-bubble">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </div>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="input-bar">
        <input
          v-model="input"
          placeholder="输入消息..."
          required
          :disabled="!isConnected"
          class="msg-input"
        />
        <button type="submit" class="send-btn" :disabled="!isConnected">发送</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../store/auth';

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
const isConnected = ref(false);
const isTyping = ref(false);
let ws: WebSocket | null = null;
const msgContainer = ref<HTMLElement | null>(null);

const initWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const token = auth.token;
  ws = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/${sessionId}?token=${encodeURIComponent(token || '')}`
  );

  ws.onopen = () => {
    isConnected.value = true;
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.role === 'assistant') {
      isTyping.value = false;
    }
    messages.value.push({ id: data.id, role: data.role, content: data.content });
    scrollToBottom();
  };

  ws.onclose = () => {
    isConnected.value = false;
  };

  ws.onerror = () => {
    isConnected.value = false;
  };
};

const sendMessage = () => {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  const content = input.value.trim();
  if (!content) return;

  ws.send(JSON.stringify({ role: 'user', content }));
  messages.value.push({ id: Date.now().toString(), role: 'user', content });
  input.value = '';
  isTyping.value = true;
  scrollToBottom();
};

const scrollToBottom = async () => {
  await nextTick();
  if (msgContainer.value) {
    msgContainer.value.scrollTop = msgContainer.value.scrollHeight;
  }
};

onMounted(() => {
  initWebSocket();
});

onBeforeUnmount(() => {
  if (ws) ws.close();
});
</script>

<style scoped>
.chat-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.chat-container {
  max-width: 720px;
  width: 100%;
  height: 88vh;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(126, 200, 160, 0.12), 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.6);
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
  border-bottom: 1px solid #A5D6A7;
}

.back-btn {
  font-size: 1rem;
  color: #43A047;
  text-decoration: none;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.back-btn:hover { background: rgba(255, 255, 255, 0.5); }

.header-title {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  color: #2E7D32;
}

.online-dot {
  width: 8px;
  height: 8px;
  background: #66BB6A;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  scroll-behavior: smooth;
}

.messages::-webkit-scrollbar { width: 5px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: #C8E6C9; border-radius: 10px; }

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #B0BEC5;
  gap: 0.5rem;
  margin-top: 4rem;
}

.empty-emoji {
  font-size: 3rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.msg {
  display: flex;
  max-width: 80%;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.msg.user { align-self: flex-end; }
.msg.assistant { align-self: flex-start; }

.msg-bubble {
  padding: 0.75rem 1.1rem;
  border-radius: 20px;
  line-height: 1.6;
}

.msg.user .msg-bubble {
  background: linear-gradient(135deg, #66BB6A, #43A047);
  color: #fff;
  border-bottom-right-radius: 6px;
  box-shadow: 0 2px 8px rgba(102, 187, 106, 0.25);
}

.msg.assistant .msg-bubble {
  background: #fff;
  color: #37474F;
  border-bottom-left-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #E8F5E9;
}

.msg-content {
  font-size: 0.95rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0.85rem 1.2rem;
}

.typing-bubble .dot {
  width: 7px; height: 7px;
  background: #B0BEC5;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.typing-bubble .dot:nth-child(2) { animation-delay: 0.2s; }
.typing-bubble .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.input-bar {
  display: flex;
  padding: 0.75rem 1.25rem;
  gap: 0.75rem;
  background: #FAFAFA;
  border-top: 1px solid #E8F5E9;
}

.msg-input {
  flex: 1;
  padding: 0.7rem 1.1rem;
  border: 2px solid #E8F5E9;
  border-radius: 20px;
  font-size: 0.95rem;
  font-family: inherit;
  outline: none;
  transition: all 0.3s ease;
  background: #fff;
}

.msg-input:focus {
  border-color: #66BB6A;
  box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.1);
}

.msg-input:disabled {
  background: #F5F5F5;
  color: #B0BEC5;
}

.send-btn {
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, #66BB6A, #43A047);
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 187, 106, 0.25);
  white-space: nowrap;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(102, 187, 106, 0.35);
}

.send-btn:disabled {
  background: #E0E0E0;
  color: #B0BEC5;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
