import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../api';

interface UserInfo {
  id: string;
  phone: string;
  nickname?: string;
  role?: string;
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'));
  const user = ref<UserInfo | null>(null);
  const ready = ref(false);

  const isAuthenticated = () => !!token.value;

  // 自动登录：用固定手机号 + 开发验证码 123456
  const autoLogin = async () => {
    if (token.value) {
      try {
        const me = await api.get('/auth/me', {
          headers: { Authorization: `Bearer ${token.value}` },
        });
        user.value = me.data;
        ready.value = true;
        return;
      } catch {
        localStorage.removeItem('access_token');
        token.value = null;
      }
    }

    try {
      const resp = await api.post('/auth/verify-otp', {
        phone: '13800000000',
        otp: '123456',
      });
      token.value = resp.data.access_token;
      user.value = resp.data.user;
      localStorage.setItem('access_token', token.value as string);
    } catch (e) {
      console.error('自动登录失败', e);
    }
    ready.value = true;
  };

  const login = async (phone: string, otp: string) => {
    const resp = await api.post('/auth/verify-otp', { phone, otp });
    token.value = resp.data.access_token;
    localStorage.setItem('access_token', token.value as string);
    const me = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${token.value}` },
    });
    user.value = me.data;
    return resp;
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
  };

  return { token, user, ready, isAuthenticated, autoLogin, login, logout };
});
