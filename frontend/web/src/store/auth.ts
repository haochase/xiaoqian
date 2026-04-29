import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from '../api';

interface UserInfo {
  id: string;
  phone: string;
  nickname?: string;
  role?: string;
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'));
  const user = ref<UserInfo | null>(null);

  const isAuthenticated = () => !!token.value;

  const login = async (phone: string, otp: string) => {
    const resp = await axios.post('/auth/verify-otp', { phone, otp });
    token.value = resp.data.access_token;
    localStorage.setItem('access_token', token.value as string);
    // fetch user profile (optional)
    const me = await axios.get('/auth/me', {
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

  return { token, user, isAuthenticated, login, logout };
});
