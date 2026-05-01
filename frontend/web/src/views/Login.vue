<template>
  <div class="page-wrapper">
    <div class="login-container">
      <div class="logo-area">
        <span class="logo-icon">🌸</span>
        <h1>小倩</h1>
        <p class="subtitle">主动式兴趣聊天助手</p>
      </div>
      <form @submit.prevent="onSubmit">
        <div class="field">
          <label for="phone">📱 手机号</label>
          <input v-model="phone" id="phone" type="tel" required placeholder="+86 138xxxx" />
        </div>
        <div class="field">
          <label for="otp">🔐 验证码</label>
          <input v-model="otp" id="otp" type="text" required placeholder="开发阶段填 123456" />
        </div>
        <button type="submit" class="login-btn">
          <span>✨ 开始聊天</span>
        </button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p class="hint">还没有账号？输入手机号自动注册</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

const phone = ref('');
const otp = ref('');
const error = ref('');
const router = useRouter();
const auth = useAuthStore();

const onSubmit = async () => {
  error.value = '';
  try {
    await auth.login(phone.value, otp.value);
    router.replace({ name: 'Dashboard' });
  } catch (e: any) {
    error.value = e.response?.data?.detail || '登录失败，请检查验证码';
  }
};
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-container {
  max-width: 420px;
  width: 100%;
  padding: 3rem 2.5rem;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(126, 200, 160, 0.15), 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.logo-area {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.5rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #66BB6A, #42A5F5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #90A4AE;
  font-weight: 400;
}

.field {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #546E7A;
}

input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 2px solid #E8F5E9;
  border-radius: 14px;
  font-size: 1rem;
  font-family: inherit;
  background: #FAFAFA;
  transition: all 0.3s ease;
  outline: none;
}

input:focus {
  border-color: #66BB6A;
  background: #fff;
  box-shadow: 0 0 0 4px rgba(102, 187, 106, 0.12);
}

.login-btn {
  margin-top: 1.5rem;
  width: 100%;
  padding: 0.9rem;
  font-size: 1.05rem;
  font-weight: 600;
  font-family: inherit;
  color: #fff;
  background: linear-gradient(135deg, #66BB6A, #43A047);
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(102, 187, 106, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(102, 187, 106, 0.4);
}

.login-btn:active {
  transform: translateY(0);
}

.error {
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  background: #FFF0F0;
  color: #E57373;
  border-radius: 10px;
  font-size: 0.9rem;
  text-align: center;
}

.hint {
  margin-top: 1.25rem;
  font-size: 0.8rem;
  color: #B0BEC5;
  text-align: center;
}
</style>
