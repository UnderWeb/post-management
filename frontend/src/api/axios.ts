// frontend/src/api/axios.ts
/**
 * Axios client configured for the application API.
 * Note: Content-Type is intentionally omitted to allow Axios to 
 * automatically set 'application/json' or 'multipart/form-data' 
 * based on the request payload.
 */
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api',
  timeout: 10000,
});

export default apiClient;
