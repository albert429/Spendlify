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

        // Load dashboard reminders
        await loadDashboardReminders();

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
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