import axios from 'axios';

// In production (Railway) Flask serves both the API and the React build from the
// same origin, so we use a relative path (/api).
// In local development (docker-compose) the backend runs on a different port, so
// set REACT_APP_API_URL=http://localhost:5001/api in your .env.development.local file.
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
  withCredentials: true, // Required for server-side session cookies
});

export default api;
