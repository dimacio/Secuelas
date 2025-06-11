import axios from 'axios';

// Create an Axios instance with a pre-configured base URL.
// The frontend (running on port 3000) will make requests to the backend (on port 5001).
// The `proxy` setting in package.json is not used in this Docker setup,
// so we specify the full URL to the backend container.
const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  withCredentials: true, // This is crucial for sending session cookies back and forth
});

export default api;
