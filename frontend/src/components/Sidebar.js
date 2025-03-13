import React from "react";
import Upload from "./Upload";
import "../style/sidebar.css";
import ClickSpark from "./SplashCursor";
const Sidebar = () => {
  return (
    
    <div className="sidebar">
      
      <h1 href="\">Chat with PDF</h1>
      <h3>Upload PDF</h3>
      <Upload />
      <ClickSpark>
      </ClickSpark>
      <footer className="sidebar-footer">By @ Trung Nguyen</footer>
    </div>
    
  );
};
export default Sidebar;
