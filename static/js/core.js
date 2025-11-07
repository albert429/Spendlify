// Global variables
let currentSection = 'dashboard';
let transactions = [];
let goals = [];
let reminders = [];
let currency = 'USD';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    loadDashboardData();
    loadTransactions();
    loadGoals();
    loadReminders();

    // Set today's date as default
    document.getElementById('transaction-date').valueAsDate = new Date();
    document.getElementById('goal-deadline').valueAsDate = new Date();
    document.getElementById('reminder-deadline').valueAsDate = new Date();
});

// Section Navigation
function showSection(section) {
    currentSection = section;

    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

    // Show selected section
    document.getElementById(section).classList.add('active');

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.closest('.nav-link').classList.add('active');

    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'transactions': 'Transactions',
        'goals': 'Savings Goals',
        'reminders': 'Bill Reminders',
        'ai-assistant': 'AI Assistant'
    };
    document.getElementById('sectionTitle').textContent = titles[section];

    // Refresh data for section
    if (section === 'transactions') loadTransactions();
    if (section === 'goals') loadGoals();
    if (section === 'reminders') loadReminders();
}

// Toggle sidebar for mobile
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('visible');
}

// Close sidebar
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('visible');
}