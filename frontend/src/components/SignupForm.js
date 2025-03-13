import React, { useState } from "react";
import axios from "axios";
import "../style/loginform.css"; // Reuse the same CSS for styling

const SignUpForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/signup", formData, {
        headers: { "Content-Type": "application/json" },
      });

      alert("Sign-up successful!");
      console.log("Response:", response.data);
    } catch (error) {
      setError(error.response?.data?.detail || "Sign-up failed. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <div className="logo">WELCOME</div>
        <h2>Sign up</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your name..."
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email..."
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password..."
              required
            />
          </div>
          <button type="submit" className="login-but">
            SIGN UP
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignUpForm;