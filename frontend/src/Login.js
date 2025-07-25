import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const { loading, error } = useSelector(state => state.auth);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    dispatch({ type: 'LOGIN_REQUEST' });
    
    try {
      // Format the data as x-www-form-urlencoded exactly as OAuth2PasswordRequestForm expects
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        // Handle FastAPI validation errors which come as an array
        if (Array.isArray(data.detail)) {
          const errorMessages = data.detail.map(err => err.msg).join(', ');
          throw new Error(errorMessages || 'Login failed');
        } else {
          throw new Error(data.detail || 'Login failed');
        }
      }
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: data.token });
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: error.message });
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <div className="login-help">
        <p>Demo credentials: username = "test", password = "password"</p>
      </div>
    </div>
  );
}

export default Login;
