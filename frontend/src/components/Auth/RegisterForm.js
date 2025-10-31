import React from "react";
import "./FormStyles.css";

function RegisterForm({
    fullName,
    setFullName,
    username,
    setUsername,
    password,
    setPassword,
    currency,
    setCurrency,
    handleRegister,
    loading,
}) {
    return (
        <form
            onSubmit={(e) => {
                e.preventDefault();
                handleRegister();
            }}
            className="auth-form"
        >
            <div className="form-group">
                <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Full Name"
                    className="form-input"
                    required
                />
            </div>

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

            <div className="form-group">
                <select
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                    className="form-input"
                    required
                >
                    <option value="">Select Currency</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                    <option value="EGP">EGP (₤)</option>
                </select>
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? "Creating Account..." : "Register"}
            </button>
        </form>
    );
}

export default RegisterForm;
