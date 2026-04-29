import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// request interceptor to inject token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
