import React from "react";
import Upload from "./Upload";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h2>Upload PDF</h2>
      <Upload />
      <footer className="sidebar-footer">By @ Trung Nguyen</footer>
    </div>
  );
};

export default Sidebar;
