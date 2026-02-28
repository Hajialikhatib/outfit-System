import axios from 'axios';

// Get API base URL from environment variable or use default
// In production, set VITE_API_BASE_URL in your .env file
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth Services
export const authService = {
  login: async (email, password) => {
    const response = await api.post('/accounts/login/', { email, password });
    if (response.data.token) {
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/accounts/register/', userData);
    return response.data;
  },

  logout: async () => {
    try {
      await api.post('/accounts/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('authToken');
  },
};

// Styles Services
export const stylesService = {
  getAll: () => api.get('/styles/'),
  getById: (id) => api.get(`/styles/${id}/`),
  create: (formData) => api.post('/styles/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update: (id, formData) => api.put(`/styles/${id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  delete: (id) => api.delete(`/styles/${id}/`),
};

// Orders Services
export const ordersService = {
  getAll: () => api.get('/orders/'),
  getById: (id) => api.get(`/orders/${id}/`),
  create: (orderData) => api.post('/orders/', orderData),
  update: (id, orderData) => api.put(`/orders/${id}/`, orderData),
  delete: (id) => api.delete(`/orders/${id}/`),
  getMyOrders: () => api.get('/orders/my-orders/'),
};

// Custom Style Requests Services
export const customStyleService = {
  getAll: () => api.get('/orders/custom-style-requests/'),
  getById: (id) => api.get(`/orders/custom-style-requests/${id}/`),
  create: (formData) => api.post('/orders/custom-style-requests/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  getMyRequests: () => api.get('/orders/my-custom-style-requests/'),
};

// Feedback Services
export const feedbackService = {
  getAll: () => api.get('/feedback/'),
  getById: (id) => api.get(`/feedback/${id}/`),
  create: (feedbackData) => api.post('/feedback/', feedbackData),
  getMyFeedback: () => api.get('/feedback/my-feedbacks/'),
};

export default api;
