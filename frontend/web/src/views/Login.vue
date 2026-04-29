<template>
  <div class="login-container">
    <h2>登录</h2>
    <form @submit.prevent="onSubmit">
      <div class="field">
        <label for="phone">手机号</label>
        <input v-model="phone" id="phone" type="tel" required placeholder="+86xxxxxxxxxx" />
      </div>
      <div class="field">
        <label for="otp">OTP</label>
        <input v-model="otp" id="otp" type="text" required placeholder="123456" />
      </div>
      <button type="submit" class="btn">登录</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
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
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}
.field {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
label {
  margin-bottom: 0.3rem;
  font-weight: 600;
}
input {
  width: 100%;
  padding: 0.5rem 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.2s;
}
input:focus {
  outline: none;
  border-color: #6366f1;
}
.btn {
  margin-top: 1rem;
  width: 100%;
  padding: 0.6rem;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}
.btn:hover {
  background: #4f46e5;
}
.error {
  margin-top: 1rem;
  color: #ef4444;
}
</style>
