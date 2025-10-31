import React, { useState, useEffect } from "react";
import { login, register, getTransactions, addTransaction, deleteTransaction } from "./utils/api";
import AuthPage from "./components/Auth/AuthPage";
import DashboardPage from "./components/Dashboard/DashboardPage";
import TransactionsPage from "./components/Transactions/TransactionsPage";
import Header from "./components/Layout/Header";
import Navigation from "./components/Layout/Navigation";
import ErrorMessage from "./components/Layout/ErrorMessage";

const SpendlifyApp = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [view, setView] = useState("login");
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [transactionForm, setTransactionForm] = useState({
    description: "",
    amount: "",
    type: "expense",
    category: "Other",
    currency: "USD",
    date: new Date().toISOString().split("T")[0],
  });

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [currency, setCurrency] = useState("USD");

  const currencySymbols = { USD: "$", EUR: "€", GBP: "£", JPY: "¥", EGP: "E£" };
  const symbol = currencySymbols[currentUser?.currency || "USD"];

  useEffect(() => {
    if (currentUser) loadTransactions();
  }, [currentUser]);

  const loadTransactions = async () => {
    try {
      const txs = await getTransactions(currentUser.username);
      setTransactions(txs);
    } catch {
      setError("Failed to load transactions");
    }
  };

  const handleLogin = async () => {
    if (!username || !password) return setError("Please enter username and password");
    setLoading(true);
    try {
      const user = await login({ username, password });
      setCurrentUser(user);
      setView("dashboard");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!username || !password || !fullName || !currency)
      return setError("Please fill in all fields");
    setLoading(true);
    try {
      const user = await register({ username, password, full_name: fullName, currency });
      setCurrentUser(user);
      setView("dashboard");
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setTransactions([]);
    setView("login");
    setError("");
  };

  const handleAddTransaction = async () => {
    if (!transactionForm.description || !transactionForm.amount || !transactionForm.date)
      return setError("Please fill in all fields");
    setLoading(true);
    try {
      const tx = { ...transactionForm, username: currentUser.username, amount: parseFloat(transactionForm.amount) };
      await addTransaction(tx);
      await loadTransactions();
      setTransactionForm({
        description: "",
        amount: "",
        type: "expense",
        category: "Other",
        currency: currentUser.currency,
        date: new Date().toISOString().split("T")[0],
      });
      setView("transactions");
    } catch (err) {
      setError(err.message || "Failed to add transaction");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTransaction = async (id) => {
    setLoading(true);
    try {
      await deleteTransaction(id);
      await loadTransactions();
    } catch (err) {
      setError(err.message || "Failed to delete transaction");
    } finally {
      setLoading(false);
    }
  };

  const totalIncome = transactions.filter(t => t.type === "income").reduce((s, t) => s + Number(t.amount), 0);
  const totalExpense = transactions.filter(t => t.type === "expense").reduce((s, t) => s + Number(t.amount), 0);
  const balance = totalIncome - totalExpense;

  if (!currentUser) {
    return (
      <AuthPage
        view={view}
        setView={setView}
        error={error}
        loading={loading}
        username={username}
        setUsername={setUsername}
        password={password}
        setPassword={setPassword}
        fullName={fullName}
        setFullName={setFullName}
        currency={currency}
        setCurrency={setCurrency}
        handleLogin={handleLogin}
        handleRegister={handleRegister}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentUser={currentUser} handleLogout={handleLogout} />
      <Navigation view={view} setView={setView} />
      {error && <ErrorMessage error={error} />}
      <main className="flex-1 p-6">
        {view === "dashboard" && (
          <DashboardPage symbol={symbol} balance={balance} totalIncome={totalIncome} totalExpense={totalExpense} />
        )}
        {view === "transactions" && (
          <TransactionsPage
            transactionForm={transactionForm}
            setTransactionForm={setTransactionForm}
            handleAddTransaction={handleAddTransaction}
            loading={loading}
            symbol={symbol}
          />
        )}
      </main>
    </div>
  );
};

export default SpendlifyApp;
