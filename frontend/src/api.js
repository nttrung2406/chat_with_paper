import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_BASE}/pdf/upload/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const chatWithRAG = async (message) => {
  return axios.post(`${API_BASE}/chat/`, { query: message });
};
