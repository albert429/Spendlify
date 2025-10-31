import React from "react";
import { Wallet } from "lucide-react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import "./AuthPage.css"; // ✅ import CSS file

function AuthPage({
    view,
    setView,
    error,
    loading,
    username,
    setUsername,
    password,
    setPassword,
    fullName,
    setFullName,
    currency,
    setCurrency,
    handleLogin,
    handleRegister,
}) {
    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <div className="wallet-icon">
                        <Wallet size={50} color="#fff" />
                    </div>
                    <h1 className="auth-title">Spendlify</h1>
                    <p className="auth-subtitle">Your Personal Finance Manager</p>
                </div>

                <div className="toggle">
                    <button
                        onClick={() => setView("login")}
                        className={view === "login" ? "active" : ""}
                    >
                        Login
                    </button>
                    <button
                        onClick={() => setView("register")}
                        className={view === "register" ? "active" : ""}
                    >
                        Register
                    </button>
                </div>

                {error && <div className="error-box">{error}</div>}

                <div className="form-wrapper fade-in">
                    {view === "login" ? (
                        <LoginForm
                            username={username}
                            setUsername={setUsername}
                            password={password}
                            setPassword={setPassword}
                            handleLogin={handleLogin}
                            loading={loading}
                        />
                    ) : (
                        <RegisterForm
                            fullName={fullName}
                            setFullName={setFullName}
                            username={username}
                            setUsername={setUsername}
                            password={password}
                            setPassword={setPassword}
                            currency={currency}
                            setCurrency={setCurrency}
                            handleRegister={handleRegister}
                            loading={loading}
                        />
                    )}
                </div>
            </div>
        </div>
    );
}

export default AuthPage;
