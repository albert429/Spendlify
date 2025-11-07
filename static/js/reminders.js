async function loadReminders() {
    try {
        const response = await fetch('/api/reminders');
        if (!response.ok) {
            throw new Error('Failed to load reminders');
        }
        reminders = await response.json();
        renderReminders();
    } catch (error) {
        console.error('Error loading reminders:', error);
        const tbody = document.getElementById('reminders-tbody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="4" class="empty-state"><div class="icon">⚠️</div><p>Error loading reminders</p></td></tr>';
        }
    }
}

function renderReminders() {
    const tbody = document.getElementById('reminders-tbody');

    if (!tbody) {
        console.error('Reminders tbody not found');
        return;
    }

    if (!reminders || reminders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-state"><div class="icon">🔔</div><p>No reminders set</p></td></tr>';
        return;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Sort reminders by deadline
    const sortedReminders = [...reminders].sort((a, b) => {
        return new Date(a.deadline) - new Date(b.deadline);
    });

    tbody.innerHTML = sortedReminders.map(reminder => {
        const reminderJson = JSON.stringify(reminder).replace(/"/g, '&quot;').replace(/'/g, '&#39;');

        // Calculate days left
        const deadline = new Date(reminder.deadline);
        deadline.setHours(0, 0, 0, 0);
        const timeDiff = deadline.getTime() - today.getTime();
        const daysLeft = Math.ceil(timeDiff / (1000 * 3600 * 24));

        const { dueClass, statusText } = calculateReminderStatus(daysLeft);

        return `
        <tr class="${dueClass}">
            <td>
                <strong>${reminder.title || 'Untitled'}</strong>
                ${daysLeft < 0 ? '<span style="color: #dc3545; font-size: 0.85em; display: block;">⚠️ OVERDUE</span>' :
                daysLeft === 0 ? '<span style="color: #ff4500; font-size: 0.85em; display: block;">🔴 DUE TODAY</span>' :
                    daysLeft <= 3 ? '<span style="color: #ffa500; font-size: 0.85em; display: block;">⚡ DUE SOON</span>' : ''}
            </td>
            <td><strong>$${parseFloat(reminder.amount || 0).toFixed(2)}</strong></td>
            <td>
                <div>${reminder.deadline}</div>
                <div style="font-size: 0.85em; color: #6c757d;">
                    ${daysLeft < 0 ? `${Math.abs(daysLeft)} days overdue` :
                daysLeft === 0 ? 'Today' :
                    daysLeft === 1 ? 'Tomorrow' :
                        `${daysLeft} days left`}
                </div>
            </td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-sm btn-edit" onclick='openEditReminderModal(${reminderJson})'>Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteReminder('${reminder.id}')">Delete</button>
                </div>
            </td>
        </tr>
    `;
    }).join('');
}

function openEditReminderModal(reminder) {
    console.log('Editing reminder:', reminder);

    const modal = document.getElementById('reminderModal');
    const title = document.getElementById('reminderModalTitle');

    if (!modal || !title) {
        console.error('Reminder modal elements not found');
        alert('Error: Reminder modal not found. Please refresh the page.');
        return;
    }

    title.textContent = 'Edit Reminder';

    const fields = {
        'reminder-id': reminder.id,
        'reminder-title': reminder.title,
        'reminder-amount': reminder.amount,
        'reminder-deadline': reminder.deadline
    };

    for (const [id, value] of Object.entries(fields)) {
        const element = document.getElementById(id);
        if (element) {
            element.value = value || '';
        } else {
            console.warn(`Element ${id} not found`);
        }
    }

    modal.classList.add('show');
}

function openAddReminderModal() {
    const modal = document.getElementById('reminderModal');
    const title = document.getElementById('reminderModalTitle');
    const form = document.getElementById('reminderForm');
    const idField = document.getElementById('reminder-id');

    if (!modal || !title || !form || !idField) {
        console.error('Reminder modal elements not found');
        alert('Error: Modal elements not found. Please refresh the page.');
        return;
    }

    title.textContent = 'Add Reminder';
    idField.value = '';
    form.reset();

    // Set default deadline to next week
    const nextWeek = new Date();
    nextWeek.setDate(nextWeek.getDate() + 7);
    document.getElementById('reminder-deadline').valueAsDate = nextWeek;

    modal.classList.add('show');
}

async function handleReminderSubmit(e) {
    e.preventDefault();

    const reminderId = document.getElementById('reminder-id').value;
    const data = {
        title: document.getElementById('reminder-title').value.trim(),
        amount: parseFloat(document.getElementById('reminder-amount').value),
        deadline: document.getElementById('reminder-deadline').value
    };

    // Validation
    if (!data.title) {
        alert('Please enter a reminder title');
        return;
    }

    if (!data.amount || data.amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }

    if (!data.deadline) {
        alert('Please select a deadline');
        return;
    }

    try {
        const url = reminderId ? `/api/reminders/${reminderId}` : '/api/reminders';
        const method = reminderId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal('reminderModal');
            await loadReminders();
            await loadDashboardReminders();
            alert(reminderId ? 'Reminder updated successfully!' : 'Reminder added successfully!');
        } else {
            const error = await response.json();
            alert('Error saving reminder: ' + (error.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving reminder:', error);
        alert('Error saving reminder. Please try again.');
    }
}

async function deleteReminder(id) {
    if (!confirm('Are you sure you want to delete this reminder?')) return;

    try {
        const response = await fetch(`/api/reminders/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await loadReminders();
            await loadDashboardReminders();
            alert('Reminder deleted successfully!');
        } else {
            alert('Error deleting reminder');
        }
    } catch (error) {
        console.error('Error deleting reminder:', error);
        alert('Error deleting reminder. Please try again.');
    }
}