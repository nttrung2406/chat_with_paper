import React, { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";
import Upload from "./Upload";
import "../style/sidebar.css";
import ClickSpark from "./SplashCursor";
import { jwtDecode } from "jwt-decode";

const Sidebar = () => {
  const [user, setUser] = useState(null);
  const [chatSessions, setChatSessions] = useState([]); // Stores chat history
  const [currentChat, setCurrentChat] = useState(null); // Active chat session
  // const navigate = useNavigate();

  useEffect(() => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const decoded = jwtDecode(token);
          setUser(decoded.name || decoded.sub.split("@")[0]); 
        } catch (error) {
          console.error("Error decoding token:", error);
          localStorage.removeItem("token");
        }
      }
    }, []);

  const handleNewChat = (pdfName) => {
    const newChat = { id: Date.now(), name: pdfName || "Untitled Chat" };
    setChatSessions((prev) => [...prev, newChat]);
    setCurrentChat(newChat.id);
  };

  const handleChatClick = (chatId) => {
    setCurrentChat(chatId);
  };

  return (
    <div className="sidebar">
      <ClickSpark>
        <h1>Chat with PDF</h1>

        {user ? (
          <>
            {/* <h3>Chat History</h3>
            <div className="chat-history">
              {chatSessions.length > 0 ? (
                chatSessions.map((chat) => (
                  <button
                    key={chat.id}
                    className={`chat-session ${chat.id === currentChat ? "active" : ""}`}
                    onClick={() => handleChatClick(chat.id)}
                  >
                    {chat.name}
                  </button>
                ))
              ) : (
                <p>No chats yet</p>
              )}
            </div> */}

            <h3>Upload PDF</h3>
            <Upload onUpload={handleNewChat} />
{/* 
            <button className="new-chat-button" onClick={() => handleNewChat("New Chat")}>
              New Chat
            </button> */}
          </>
        ) : (
          <p>Please log in to use PDF function.</p>
        )}
      </ClickSpark>

      <footer className="sidebar-footer">By @ Trung Nguyen</footer>
    </div>
  );
};

export default Sidebar;
