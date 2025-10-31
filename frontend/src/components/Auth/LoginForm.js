import React from "react";
import "./FormStyles.css";

function LoginForm({ username, setUsername, password, setPassword, handleLogin, loading }) {
    return (
        <form
            onSubmit={(e) => {
                e.preventDefault();
                handleLogin();
            }}
            className="auth-form"
        >
            <div className="form-group">
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    className="form-input"
                    required
                />
            </div>

            <div className="form-group">
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    className="form-input"
                    required
                />
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? "Logging in..." : "Login"}
            </button>
        </form>
    );
}

export default LoginForm;
