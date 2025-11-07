// Global variables
let currentSection = 'dashboard';
let transactions = [];
let goals = [];
let reminders = [];
let currency = 'USD';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initializing application...');

    // Load all data
    loadDashboardData();
    loadTransactions();
    loadGoals();
    loadReminders();

    // Set today's date as default for forms
    const today = new Date();

    const txDate = document.getElementById('transaction-date');
    if (txDate) txDate.valueAsDate = today;

    const goalDeadline = document.getElementById('goal-deadline');
    if (goalDeadline) {
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + 30);
        goalDeadline.valueAsDate = futureDate;
    }

    const reminderDeadline = document.getElementById('reminder-deadline');
    if (reminderDeadline) {
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + 7);
        reminderDeadline.valueAsDate = futureDate;
    }
});

// Section Navigation
function showSection(section) {
    console.log('Switching to section:', section);
    currentSection = section;

    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

    // Show selected section
    const sectionElement = document.getElementById(section);
    if (sectionElement) {
        sectionElement.classList.add('active');
    } else {
        console.error(`Section ${section} not found`);
        return;
    }

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    if (event && event.target) {
        const clickedLink = event.target.closest('.nav-link');
        if (clickedLink) {
            clickedLink.classList.add('active');
        }
    }

    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'transactions': 'Transactions',
        'goals': 'Savings Goals',
        'reminders': 'Bill Reminders',
        'ai-assistant': 'AI Assistant'
    };
    const titleElement = document.getElementById('sectionTitle');
    if (titleElement) {
        titleElement.textContent = titles[section] || 'Dashboard';
    }

    // Refresh data for section
    if (section === 'transactions') {
        loadTransactions();
    } else if (section === 'goals') {
        loadGoals();
    } else if (section === 'reminders') {
        loadReminders();
    } else if (section === 'dashboard') {
        loadDashboardData();
    }

    // Close sidebar on mobile
    closeSidebar();
}

// Toggle sidebar for mobile
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const mainContent = document.getElementById('mainContent');

    if (sidebar) {
        sidebar.classList.toggle('visible');
    }

    if (overlay) {
        overlay.classList.toggle('show');
    }

    if (mainContent) {
        mainContent.classList.toggle('expanded');
    }
}

// Close sidebar
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const mainContent = document.getElementById('mainContent');

    if (sidebar) {
        sidebar.classList.remove('visible');
    }

    if (overlay) {
        overlay.classList.remove('show');
    }

    if (mainContent && window.innerWidth <= 768) {
        mainContent.classList.add('expanded');
    }
}

// Close modal helper
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Click outside modal to close
window.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
});

// Handle window resize
window.addEventListener('resize', function () {
    const mainContent = document.getElementById('mainContent');
    if (window.innerWidth > 768) {
        closeSidebar();
        if (mainContent) {
            mainContent.classList.remove('expanded');
        }
    }
});

// Utility function to format currency
function formatCurrency(amount, currencyCode = 'USD') {
    const symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'EGP': 'E£'
    };

    const symbol = symbols[currencyCode] || currencyCode;
    return `${symbol}${parseFloat(amount).toFixed(2)}`;
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Error handler
function handleError(error, context = '') {
    console.error(`Error in ${context}:`, error);
    alert(`An error occurred${context ? ' in ' + context : ''}. Please try again.`);
}

// Success message
function showSuccess(message) {
    // You can implement a toast notification here
    console.log('Success:', message);
}