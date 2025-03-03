import React, { useState } from "react";
import { chatWithRAG } from "../api";

const Chatbox = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = { sender: "user", text: message };
    setChatHistory([...chatHistory, userMessage]);

    try {
      const response = await chatWithRAG(message);
      const botMessage = { sender: "bot", text: response.data.answer };
      setChatHistory([...chatHistory, userMessage, botMessage]);
    } catch (error) {
      console.error("Chat failed:", error);
    }

    setMessage("");
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {chatHistory.map((msg, index) => (
          <div key={index} className={msg.sender}>
            <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbox;
