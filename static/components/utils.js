// Utility functions
function calculateReminderStatus(daysLeft) {
    let dueClass, statusText;

    if (daysLeft < 0) {
        dueClass = 'overdue';
        statusText = 'OVERDUE';
    } else if (daysLeft === 0) {
        dueClass = 'due-today';
        statusText = 'TODAY';
    } else if (daysLeft === 1) {
        dueClass = 'due-soon';
        statusText = 'TOMORROW';
    } else if (daysLeft <= 3) {
        dueClass = 'due-soon';
        statusText = `${daysLeft} DAYS`;
    } else if (daysLeft <= 5) {
        dueClass = 'due-approaching';
        statusText = `${daysLeft} DAYS`;
    } else {
        dueClass = 'due-later';
        statusText = `${daysLeft} DAYS`;
    }

    return { dueClass, statusText };
}

// Helper function to format date as "MMM DD"
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}