// Chart instances
let categoryChart = null;
let trendChart = null;

// Dashboard Data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/summary');
        const data = await response.json();

        currency = data.currency;

        // Currency symbols
        const symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'EGP': 'E£'
        };
        const symbol = symbols[currency] || '';

        // Update stats
        document.getElementById('total-income').textContent =
            `${symbol}${data.income.toFixed(2)}`;
        document.getElementById('total-expense').textContent =
            `${symbol}${data.expense.toFixed(2)}`;
        document.getElementById('net-balance').textContent =
            `${symbol}${data.net.toFixed(2)}`;

        // Update top categories
        const categoriesHtml = data.top_categories.length > 0
            ? data.top_categories.map(cat => `
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>${cat.category}</span>
                        <span><strong>${symbol}${cat.amount.toFixed(2)}</strong> (${cat.percent.toFixed(1)}%)</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${cat.percent}%"></div>
                    </div>
                </div>
            `).join('')
            : '<div class="empty-state"><div class="icon">📊</div><p>No expense data yet</p></div>';

        document.getElementById('top-categories').innerHTML = categoriesHtml;

        // Load recent transactions for dashboard
        const txResponse = await fetch('/api/transactions');
        const allTx = await txResponse.json();
        const recentTx = allTx.slice(-5).reverse();

        const recentHtml = recentTx.length > 0
            ? `<div class="table-container"><table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    ${recentTx.map(tx => `
                        <tr>
                            <td>${tx.date}</td>
                            <td>${tx.description}</td>
                            <td>${tx.currency} ${parseFloat(tx.amount).toFixed(2)}</td>
                            <td><span class="badge badge-${tx.type}">${tx.type}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table></div>`
            : '<div class="empty-state"><div class="icon">💳</div><p>No transactions yet</p></div>';

        document.getElementById('recent-transactions').innerHTML = recentHtml;

        // Render charts
        renderCategoryChart(data.top_categories, allTx);
        renderTrendChart(allTx);

        // Load dashboard reminders
        await loadDashboardReminders();

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Render Category Pie Chart
function renderCategoryChart(categories, transactions) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    // Destroy existing chart
    if (categoryChart) {
        categoryChart.destroy();
    }

    // Get expense transactions only
    const expenses = transactions.filter(tx => tx.type === 'expense');
    
    // Group by category
    const categoryData = {};
    expenses.forEach(tx => {
        const cat = tx.category || 'Other';
        categoryData[cat] = (categoryData[cat] || 0) + parseFloat(tx.amount);
    });

    const labels = Object.keys(categoryData);
    const data = Object.values(categoryData);

    if (labels.length === 0) {
        ctx.parentElement.innerHTML = '<div class="empty-state" style="padding: 40px;"><p>No expense data to visualize</p></div>';
        return;
    }

    // Modern color palette
    const colors = [
        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6',
        '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
    ];

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: $${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Render Monthly Trend Line Chart
function renderTrendChart(transactions) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;

    // Destroy existing chart
    if (trendChart) {
        trendChart.destroy();
    }

    if (transactions.length === 0) {
        ctx.parentElement.innerHTML = '<div class="empty-state" style="padding: 40px;"><p>No transaction data to visualize</p></div>';
        return;
    }

    // Group transactions by month
    const monthlyData = {};
    transactions.forEach(tx => {
        const date = new Date(tx.date);
        const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        
        if (!monthlyData[monthKey]) {
            monthlyData[monthKey] = { income: 0, expense: 0 };
        }
        
        const amount = parseFloat(tx.amount);
        if (tx.type === 'income') {
            monthlyData[monthKey].income += amount;
        } else {
            monthlyData[monthKey].expense += amount;
        }
    });

    // Sort by month and get last 6 months
    const sortedMonths = Object.keys(monthlyData).sort().slice(-6);
    const labels = sortedMonths.map(m => {
        const [year, month] = m.split('-');
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    });

    const incomeData = sortedMonths.map(m => monthlyData[m].income);
    const expenseData = sortedMonths.map(m => monthlyData[m].expense);

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Income',
                    data: incomeData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Expenses',
                    data: expenseData,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

// Dashboard Reminders
async function loadDashboardReminders() {
    try {
        const response = await fetch('/api/reminders');
        const reminders = await response.json();
        renderDashboardReminders(reminders);
    } catch (error) {
        console.error('Error loading dashboard reminders:', error);
    }
}

function renderDashboardReminders(reminders) {
    const container = document.getElementById('dashboard-reminders');

    if (!reminders || reminders.length === 0) {
        container.innerHTML = `
            <div class="empty-reminders">
                <div class="icon">📅</div>
                <p>No upcoming bills</p>
                <p class="subtext">Add bill reminders to track upcoming payments</p>
            </div>
        `;
        return;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Sort reminders by due date (soonest first)
    const sortedReminders = [...reminders].sort((a, b) => {
        const dateA = new Date(a.deadline);
        const dateB = new Date(b.deadline);
        return dateA - dateB;
    });

    const html = `
        <div class="reminders-horizontal">
            ${sortedReminders.map(reminder => {
        const deadline = new Date(reminder.deadline);
        deadline.setHours(0, 0, 0, 0);

        const timeDiff = deadline.getTime() - today.getTime();
        const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));

        const { dueClass, statusText } = calculateReminderStatus(daysLeft);

        return `
                    <div class="reminder-card-horizontal ${dueClass}">
                        <div class="reminder-card-header">
                            <div class="reminder-card-title">${reminder.title}</div>
                            <div class="reminder-card-amount">$${parseFloat(reminder.amount).toFixed(2)}</div>
                        </div>
                        <div class="reminder-card-details">
                            <div class="reminder-card-date">${formatDate(reminder.deadline)}</div>
                            <div class="reminder-card-status">${statusText}</div>
                        </div>
                    </div>
                `;
    }).join('')}
        </div>
    `;

    container.innerHTML = html;
}