import React from "react";
import Sidebar from "./components/Sidebar";
import Chatbox from "./components/Chatbox";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Sidebar />
      <Chatbox />
    </div>
  );
}

export default App;
