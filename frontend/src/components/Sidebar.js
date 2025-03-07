import React from "react";
import Upload from "./Upload";
import "../style/sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h1>Chat with PDF</h1>
      <h2>Upload PDF</h2>
      <Upload />
      <footer className="sidebar-footer">By @ Trung Nguyen</footer>
    </div>
  );
};

export default Sidebar;
