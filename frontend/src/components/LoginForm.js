import React, { useState } from "react";
import axios from "axios";
import '../style/loginform.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    login: '',
    password: '',
    mfaCode: '',
    rememberMe: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);

    try {
      const response = await axios.post('/api/auth/login', formData);
      console.log('Login successful:', response.data);
    } catch (error) {
      console.error('Login failed:', error.response ? error.response.data : error.message);
    }
  };


  return (
    <div className="login-container">
      <div className="login-form">
        <div className="logo">AA</div>
        <h2>Sign in to dashboard</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="login">Login</label>
            <input
              type="text"
              id="login"
              name="login"
              value={formData.login}
              onChange={handleChange}
              placeholder="Enter your login..."
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
          <div className="form-group">
            <label htmlFor="mfaCode">MFA Code</label>
            <input
              type="text"
              id="mfaCode"
              name="mfaCode"
              value={formData.mfaCode}
              onChange={handleChange}
              placeholder="Enter your code..."
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
              />{' '}
              Remember me
            </label>
            <a href="#forgot-password">Forgot password?</a>
          </div>
          <button type="submit" className="login-button">
            LOGIN
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;