const BASE = 'http://localhost:5000';

async function request(path, opts = {}) {
  const res = await fetch(BASE + path, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      ...(opts.headers || {})
    },
    mode: 'cors'
  });
  if (res.status === 204) return null;
  const txt = await res.text();
  try { return JSON.parse(txt || 'null'); } catch { return txt; }
}

export async function login({ username, password }) {
  return request('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  });
}

export async function register({ username, password, full_name, currency }) {
  return request('/register', {
    method: 'POST',
    body: JSON.stringify({ username, password, full_name, currency })
  });
}

export async function getTransactions(username) {
  return request(`/transactions?user=${encodeURIComponent(username)}`, { method: 'GET' }) || [];
}

export async function addTransaction(tx) {
  return request('/transactions/add', { method: 'POST', body: JSON.stringify(tx) });
}

export async function editTransaction(id, tx) {
  return request('/transactions/edit', { method: 'POST', body: JSON.stringify({ id, ...tx }) });
}

export async function deleteTransaction(id) {
  return request(`/transactions/delete?id=${encodeURIComponent(id)}`, { method: 'DELETE' });
}

export async function getGoals(username) {
  return request(`/goals?user=${encodeURIComponent(username)}`, { method: 'GET' }) || [];
}

export async function addGoal(goal) {
  return request('/goals/add', { method: 'POST', body: JSON.stringify(goal) });
}

export async function getReminders(username) {
  return request(`/reminders?user=${encodeURIComponent(username)}`, { method: 'GET' }) || [];
}

export async function addReminder(rem) {
  return request('/reminders/add', { method: 'POST', body: JSON.stringify(rem) });
}
