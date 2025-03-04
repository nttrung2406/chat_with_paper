import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; 

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_BASE}/pdf/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};



export async function chatWithRAG(prompt) {
  try {
      const response = await fetch("http://127.0.0.1:8000/chat/text", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      if (!data.answer) {
          throw new Error("Invalid response structure from backend");
      }

      return data.answer; 
  } catch (error) {
      console.error("Chat failed:", error);
      return "Error: Unable to get a response from the server.";
  }
}
