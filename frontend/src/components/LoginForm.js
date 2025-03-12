import React, { useState } from "react";
import axios from "axios";
import "../style/loginform.css";

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rememberMe: false,
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); 

    try {
      const loginData = new URLSearchParams();
      loginData.append("username", formData.username);
      loginData.append("password", formData.password);

      const response = await axios.post("http://127.0.0.1:8000/token", loginData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      alert("Login successful!");
      console.log("Token:", access_token);
    } catch (error) {
      setError(error.response?.data?.detail || "Login failed. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <div className="logo">WELCOME</div>
        <h2>Log in</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username..."
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
          <div className="form-options">
            <label>
              <input
                type="checkbox"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
              />{" "}
              Remember me
            </label>
            <a href="#forgot-password">Forgot password?</a>
          </div>
          <button type="submit" className="login-but">
            LOGIN
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
