import axios from "axios";

// When VITE_API_BASE_URL is empty we rely on the Vite dev proxy ("/api").
const baseURL = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

// Attach a bearer token if one is stored.
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
