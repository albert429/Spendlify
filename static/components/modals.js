// Modal functions
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Close modal when clicking outside
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

// Form submission handlers (to be called from HTML)
function handleTransactionSubmit(e) {
    e.preventDefault();
    // Implementation in transactions.js
}

function handleGoalSubmit(e) {
    e.preventDefault();
    // Implementation in goals.js
}

function handleReminderSubmit(e) {
    e.preventDefault();
    // Implementation in reminders.js
}