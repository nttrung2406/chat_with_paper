import React from "react";
import { BrowserRouter as Router, Route, Routes, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Chatbox from "./components/Chatbox";
import LoginForm from "./components/LoginForm";
import LogPage from "./components/LogPage";
import "./App.css";

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

function AppContent() {
  const location = useLocation();
  const hideSidebar = location.pathname === "/login";

  return (
    <div className="app">
      {!hideSidebar && <Sidebar />}
      <Routes>
        <Route path="/" element={<Chatbox />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/logs" element={<LogPage />} />
      </Routes>
    </div>
  );
}

export default App;