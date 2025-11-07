// Transactions
async function loadTransactions() {
    try {
        const response = await fetch('/api/transactions');
        transactions = await response.json();
        renderTransactions();
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function renderTransactions() {
    const tbody = document.getElementById('transactions-tbody');

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="icon">💳</div><p>No transactions yet</p></td></tr>';
        return;
    }

    tbody.innerHTML = transactions.map(tx => `
        <tr>
            <td>${tx.date}</td>
            <td>${tx.description}</td>
            <td>${tx.category}</td>
            <td>${tx.currency} ${parseFloat(tx.amount).toFixed(2)}</td>
            <td><span class="badge badge-${tx.type}">${tx.type}</span></td>
            <td>${tx.payment}</td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-sm btn-edit" onclick='editTransaction(${JSON.stringify(tx)})'>Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteTransaction('${tx.id}')">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function openAddTransactionModal() {
    document.getElementById('transactionModalTitle').textContent = 'Add Transaction';
    document.getElementById('transactionForm').reset();
    document.getElementById('transaction-id').value = '';
    document.getElementById('transaction-date').valueAsDate = new Date();
    document.getElementById('transactionModal').classList.add('show');
}

function editTransaction(tx) {
    document.getElementById('transactionModalTitle').textContent = 'Edit Transaction';
    document.getElementById('transaction-id').value = tx.id;
    document.getElementById('transaction-amount').value = tx.amount;
    document.getElementById('transaction-currency').value = tx.currency;
    document.getElementById('transaction-category').value = tx.category;
    document.getElementById('transaction-date').value = tx.date;
    document.getElementById('transaction-description').value = tx.description;
    document.getElementById('transaction-type').value = tx.type;
    document.getElementById('transaction-payment').value = tx.payment;
    document.getElementById('transactionModal').classList.add('show');
}

async function handleTransactionSubmit(e) {
    e.preventDefault();

    const txId = document.getElementById('transaction-id').value;
    const data = {
        amount: document.getElementById('transaction-amount').value,
        currency: document.getElementById('transaction-currency').value,
        category: document.getElementById('transaction-category').value,
        date: document.getElementById('transaction-date').value,
        description: document.getElementById('transaction-description').value,
        type: document.getElementById('transaction-type').value,
        payment: document.getElementById('transaction-payment').value
    };

    try {
        const url = txId ? `/api/transactions/${txId}` : '/api/transactions';
        const method = txId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal('transactionModal');
            loadTransactions();
            loadDashboardData();
        }
    } catch (error) {
        console.error('Error saving transaction:', error);
    }
}

async function deleteTransaction(id) {
    if (!confirm('Are you sure you want to delete this transaction?')) return;

    try {
        const response = await fetch(`/api/transactions/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadTransactions();
            loadDashboardData();
        }
    } catch (error) {
        console.error('Error deleting transaction:', error);
    }
}

// CSV Import/Export functions
function importCSV(event) {
    // TODO: Implement CSV import functionality
    console.log('Import CSV functionality to be implemented');
    event.preventDefault();
}

function exportCSV() {
    // TODO: Implement CSV export functionality
    console.log('Export CSV functionality to be implemented');
}