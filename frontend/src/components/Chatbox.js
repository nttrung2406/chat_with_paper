import React, { useState } from "react";
import { chatWithRAG } from "../api";

const Chatbox = () => {
  const [message, setMessage] = useState("");  
  const [chatHistory, setChatHistory] = useState([]); 

  async function handleSend() {
    const userMessage = message.trim();
    if (!userMessage) return;

    setChatHistory((prev) => [...prev, { sender: "user", text: userMessage }]);

    try {
      const botResponse = await chatWithRAG(userMessage);

      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: botResponse || "No response from server" },
      ]);
    } catch (error) {
      console.error("Error in handleSend:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Error: Unable to get a response." },
      ]);
    }

    setMessage(""); 
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
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
          onKeyDown={handleKeyPress}
          placeholder="Ask something..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbox;
