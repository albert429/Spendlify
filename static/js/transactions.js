async function loadTransactions() {
    try {
        const response = await fetch('/api/transactions');
        if (!response.ok) {
            throw new Error('Failed to load transactions');
        }
        transactions = await response.json();
        renderTransactions();
    } catch (error) {
        console.error('Error loading transactions:', error);
        const tbody = document.getElementById('transactions-tbody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="icon">⚠️</div><p>Error loading transactions</p></td></tr>';
        }
    }
}

function renderTransactions() {
    const tbody = document.getElementById('transactions-tbody');

    if (!tbody) {
        console.error('Transactions tbody not found');
        return;
    }

    if (!transactions || transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="icon">💳</div><p>No transactions yet</p></td></tr>';
        return;
    }

    // Sort by date (newest first)
    const sortedTransactions = [...transactions].sort((a, b) => {
        return new Date(b.date) - new Date(a.date);
    });

    tbody.innerHTML = sortedTransactions.map(tx => {
        // Safely escape JSON for HTML attribute
        const txJson = JSON.stringify(tx).replace(/"/g, '&quot;');
        return `
        <tr>
            <td>${tx.date || 'N/A'}</td>
            <td>${tx.description || 'N/A'}</td>
            <td><span class="category-badge category-${(tx.category || 'other').toLowerCase()}">${tx.category || 'Other'}</span></td>
            <td class="amount-${tx.type || 'expense'}">${tx.currency || 'USD'} ${parseFloat(tx.amount || 0).toFixed(2)}</td>
            <td><span class="badge badge-${tx.type || 'expense'}">${tx.type || 'expense'}</span></td>
            <td>${tx.payment || 'N/A'}</td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-sm btn-edit" onclick='openEditTransactionModal(${txJson})'>Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteTransaction('${tx.id}')">Delete</button>
                </div>
            </td>
        </tr>
    `;
    }).join('');
}

function openAddTransactionModal() {
    const modal = document.getElementById('transactionModal');
    const form = document.getElementById('transactionForm');
    const title = document.getElementById('transactionModalTitle');

    if (!modal || !form || !title) {
        console.error('Transaction modal elements not found');
        return;
    }

    title.textContent = 'Add Transaction';
    form.reset();
    document.getElementById('transaction-id').value = '';
    document.getElementById('transaction-date').valueAsDate = new Date();
    document.getElementById('transaction-currency').value = currency || 'USD';
    modal.classList.add('show');
}

function openEditTransactionModal(tx) {
    console.log('Opening edit transaction modal for:', tx);

    const modal = document.getElementById('transactionModal');
    const title = document.getElementById('transactionModalTitle');

    if (!modal || !title) {
        console.error('Transaction modal elements not found');
        alert('Error: Modal not found. Please refresh the page.');
        return;
    }

    // Set modal title
    title.textContent = 'Edit Transaction';

    // Populate form fields
    const fields = {
        'transaction-id': tx.id,
        'transaction-amount': tx.amount,
        'transaction-currency': tx.currency,
        'transaction-category': tx.category,
        'transaction-date': tx.date,
        'transaction-description': tx.description,
        'transaction-type': tx.type,
        'transaction-payment': tx.payment
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

async function handleTransactionSubmit(e) {
    e.preventDefault();

    const txId = document.getElementById('transaction-id').value;
    const data = {
        amount: parseFloat(document.getElementById('transaction-amount').value),
        currency: document.getElementById('transaction-currency').value,
        category: document.getElementById('transaction-category').value,
        date: document.getElementById('transaction-date').value,
        description: document.getElementById('transaction-description').value,
        type: document.getElementById('transaction-type').value,
        payment: document.getElementById('transaction-payment').value
    };

    // Validation
    if (!data.amount || data.amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }

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
            await loadTransactions();
            await loadDashboardData();
            alert(txId ? 'Transaction updated successfully!' : 'Transaction added successfully!');
        } else {
            const error = await response.json();
            alert('Error saving transaction: ' + (error.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving transaction:', error);
        alert('Error saving transaction. Please try again.');
    }
}

async function deleteTransaction(id) {
    if (!confirm('Are you sure you want to delete this transaction?')) return;

    try {
        const response = await fetch(`/api/transactions/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await loadTransactions();
            await loadDashboardData();
            alert('Transaction deleted successfully!');
        } else {
            alert('Error deleting transaction');
        }
    } catch (error) {
        console.error('Error deleting transaction:', error);
        alert('Error deleting transaction. Please try again.');
    }
}

// CSV Import function
async function importCSV(event) {
    event.preventDefault();

    // Create file input element
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv';

    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/transactions/import', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Successfully imported ${result.count || 0} transactions!`);
                await loadTransactions();
                await loadDashboardData();
            } else {
                const error = await response.json();
                alert('Import failed: ' + (error.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error importing CSV:', error);
            alert('Error importing CSV. Please check the file format.');
        }
    };

    input.click();
}

// CSV Export function
async function exportCSV() {
    try {
        const response = await fetch('/api/transactions/export');

        if (!response.ok) {
            throw new Error('Export failed');
        }

        // Get the CSV content
        const blob = await response.blob();

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `transactions_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();

        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        alert('Transactions exported successfully!');
    } catch (error) {
        console.error('Error exporting CSV:', error);
        alert('Error exporting transactions. Please try again.');
    }
}