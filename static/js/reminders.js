// Reminders
async function loadReminders() {
    try {
        const response = await fetch('/api/reminders');
        reminders = await response.json();
        renderReminders();
    } catch (error) {
        console.error('Error loading reminders:', error);
    }
}

function renderReminders() {
    const tbody = document.getElementById('reminders-tbody');

    if (reminders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-state"><div class="icon">🔔</div><p>No reminders set</p></td></tr>';
        return;
    }

    tbody.innerHTML = reminders.map(reminder => `
        <tr>
            <td>${reminder.title}</td>
            <td>$${parseFloat(reminder.amount).toFixed(2)}</td>
            <td>${reminder.deadline}</td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-sm btn-edit" onclick='editReminder(${JSON.stringify(reminder)})'>Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteReminder('${reminder.id}')">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function openEditReminderModal(reminder) {
    console.log('Editing reminder:', reminder);
    document.getElementById('reminderModalTitle').textContent = 'Edit Reminder';
    document.getElementById('reminder-id').value = reminder.id;
    document.getElementById('reminder-title').value = reminder.title;
    document.getElementById('reminder-amount').value = reminder.amount;
    document.getElementById('reminder-deadline').value = reminder.deadline;
    document.getElementById('reminderModal').classList.add('show');
}

function openAddReminderModal() {
    document.getElementById('reminderModalTitle').textContent = 'Add Reminder';
    document.getElementById('reminderForm').reset();
    document.getElementById('reminder-id').value = '';
    document.getElementById('reminder-deadline').valueAsDate = new Date();
    document.getElementById('reminderModal').classList.add('show');
}

async function handleReminderSubmit(e) {
    e.preventDefault();

    const reminderId = document.getElementById('reminder-id').value;
    const data = {
        title: document.getElementById('reminder-title').value,
        amount: document.getElementById('reminder-amount').value,
        deadline: document.getElementById('reminder-deadline').value
    };

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
            loadReminders();
            loadDashboardReminders();
        }
    } catch (error) {
        console.error('Error saving reminder:', error);
    }
}

function editReminder(reminder) {
    openEditReminderModal(reminder);
}

async function deleteReminder(id) {
    if (!confirm('Are you sure you want to delete this reminder?')) return;

    try {
        const response = await fetch(`/api/reminders/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadReminders();
            loadDashboardReminders();
        }
    } catch (error) {
        console.error('Error deleting reminder:', error);
    }
}