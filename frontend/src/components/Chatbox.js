import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { chatWithRAG } from "../api";
import { jwtDecode } from "jwt-decode";
import "../style/chatbox.css";
import StarBorder from "./StarBorder";

const Chatbox = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [user, setUser] = useState(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [lastQuestion, setLastQuestion] = useState("");
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

    if (userMessage.toLowerCase() === lastQuestion.toLowerCase()) {
      console.log("Duplicate question detected. Skipping API call.");
      setMessage("");
      return;
    }
    setLastQuestion(userMessage);
    setIsLoading(true);
    setChatHistory((prev) => [...prev, { sender: "user", text: userMessage }]);
    setMessage("");

    try {
      const botResponse = await chatWithRAG(userMessage);
      // console.log("botResponse:", botResponse);

      const lastBotResponse = chatHistory.findLast((msg) => msg.sender === "bot")?.text;
      if (lastBotResponse && isSimilarResponse(botResponse, lastBotResponse)) {
        console.log("Similar response detected. Skipping adding to chat history.");
      } else {
        const shortenedResponse = userMessage.toLowerCase().includes("what is ai")
          ? shortenAIResponse(botResponse)
          : botResponse;

        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", text: shortenedResponse || "No response from server" },
        ]);
      }
    } catch (error) {
      console.error("Error in handleSend:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Error: Unable to get a response." },
      ]);
    } finally {
      setIsLoading(false);
    }
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

  const isSimilarResponse = (response1, response2) => {
    if (!response1 || !response2) return false;
    const keywords1 = response1.toLowerCase().split(/\s+/);
    const keywords2 = response2.toLowerCase().split(/\s+/);
    const commonKeywords = keywords1.filter((keyword) => keywords2.includes(keyword));
    return commonKeywords.length / Math.max(keywords1.length, keywords2.length) > 0.5;
  };

  const shortenAIResponse = (response) => {
    const sentences = response.split(". ");
    if (sentences.length > 2) {
      return sentences.slice(0, 6).join(". ") + "."; 
    }
    return response;
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
                <button className="dropdown" onClick={() => navigate("/product-info")}>
                  Product Info
                </button>
                <button className="dropdown" onClick={handleLogout}>
                  Log Out
                </button>
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
        {isLoading && (
          <div className="message bot">
            <strong>Bot:</strong> Loading...
          </div>
        )}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Ask something..."
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbox;
