import React, { useState, useEffect  } from "react";
import { useNavigate } from "react-router-dom";
import { chatWithRAG } from "../api";
import { jwtDecode } from "jwt-decode";
import "../style/chatbox.css";
import StarBorder from "./StarBorder";
import { Dropdown } from "flowbite-react";
import { HiLogout, HiViewGrid } from "react-icons/hi";
const Chatbox = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [user, setUser] = useState(null); // Store username
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        console.log("Decoded Token:", decoded);
        setUser(decoded.name || decoded.sub.split("@")[0]); 
      } catch (error) {
        console.error("Error decoding token:", error);
        localStorage.removeItem("token");
      }
    }
  }, []);

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

  const handleLoginClick = () => {
    navigate("/login");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setDropdownOpen(false);
  };

  return (
    <div className="chatbox">
      <div className="header">
        {user ? (
          <div className="user-menu">
            <StarBorder
              as="button"
              className="custom-class"
              color="black"
              speed="2s"
              onClick={() => setDropdownOpen(!dropdownOpen)}
            >
              {user}
            </StarBorder>
            {dropdownOpen && (
              <div className="dropdown">
                <button className="dropdown" onClick={() => navigate("/product-info")}>Product Info</button>
                <button className="dropdown" onClick={handleLogout}>Log Out</button>
              </div>
            )}
          </div>
        ) : (
          <button className="login-button" onClick={handleLoginClick}>
            Login
          </button>
        )}
      </div>
      <div className="messages">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
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