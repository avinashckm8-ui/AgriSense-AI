import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for consistent error messaging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred while communicating with AgriSense AI server.';
    return Promise.reject(new Error(message));
  }
);

export default api;

export const predictFertilizer = async (payload) => {
  const response = await api.post('/predict/fertilizer', payload);
  return response.data;
};

export const checkFertilizerHealth = async () => {
  const response = await api.get('/predict/fertilizer/health');
  return response.data;
};
