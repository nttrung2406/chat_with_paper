import React, { useState } from "react";
import { uploadPDF } from "../api";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }

    setStatus("Uploading...");
    try {
      const response = await uploadPDF(file);
      setStatus("Upload Successful!");
    } catch (error) {
      setStatus("Upload failed!");
      console.error(error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{status}</p>
    </div>
  );
};

export default Upload;
