import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../provider/authProvider";

import React, { useState, useRef } from "react";
import { selectLocalPeer } from "@100mslive/react-sdk";

const required = value => {
    if (!value) {
      return (
        <div className="invalid-feedback d-block">
          This field is required!
        </div>
      );
    }
};

const API_URL = "https://avalon-card-game.onrender.com";

const Login = () => {
  const { setToken, setLocalEmail } = useAuth();

  const form = useRef();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const onChangeEmail = (e) => {
    const email = e.target.value;
    setEmail(email);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    axios.post(API_URL + "/user/login", {
      email,
      password,
    })
    .then((response) => {
      if (response.data.access_token) {
        setToken(response.data.access_token);
        setLocalEmail(email);
        navigate("/", { replace: true });
      }
    });
    setLoading(false);
  };

  return (
    <div className="col-md-12">
      <div className="card card-container">
        <form onSubmit={handleLogin} ref={form}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="text"
              className="form-control"
              name="email"
              value={email}
              onChange={onChangeEmail}
              validations={[required]}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              className="form-control"
              name="password"
              value={password}
              onChange={onChangePassword}
              validations={[required]}
            />
          </div>

          <div className="form-group">
            <button className="btn btn-primary btn-block" disabled={loading}>
              {loading && (
                <span className="spinner-border spinner-border-sm"></span>
              )}
              <span>Login</span>
            </button>
          </div>

          {message && (
            <div className="form-group">
              <div className="alert alert-danger" role="alert">
                {message}
              </div>
            </div>
          )}
        </form>
        
      </div>
      <h2 className="sign-up-link"><a href="/register">Sign up</a></h2>
    </div>
  );
};

export default Login;