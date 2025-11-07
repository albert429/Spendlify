// Goals Functions
async function loadGoals() {
    try {
        const response = await fetch('/api/goals');
        goals = await response.json();
        renderGoals();
    } catch (error) {
        console.error('Error loading goals:', error);
    }
}

function renderGoals() {
    const container = document.getElementById('goals-list');

    if (!container) {
        console.error('Goals container not found');
        return;
    }

    if (goals.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="icon">🎯</div><p>No goals yet. Start setting your financial targets!</p></div>';
        return;
    }

    container.innerHTML = goals.map(goal => {
        const progress = Math.min((goal.current_amount / goal.target_amount) * 100, 100);
        const goalJson = JSON.stringify(goal).replace(/"/g, '&quot;');

        return `
            <div class="card" style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div>
                        <h4 style="margin-bottom: 5px;">${goal.title}</h4>
                        <p style="color: #666; font-size: 0.9em;">Target: $${goal.target_amount.toFixed(2)} by ${goal.deadline}</p>
                    </div>
                    <span class="badge badge-${goal.status}">${goal.status}</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>Progress</span>
                        <span><strong>$${goal.current_amount.toFixed(2)}</strong> / $${goal.target_amount.toFixed(2)}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${progress}%"></div>
                    </div>
                    <div style="text-align: right; margin-top: 5px; color: #666; font-size: 0.9em;">
                        ${progress.toFixed(1)}% Complete
                    </div>
                </div>
                <div class="action-btns">
                    <button class="btn btn-sm btn-edit" onclick="openEditGoalModal(${goalJson})">Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteGoal('${goal.id}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function openEditGoalModal(goal) {
    console.log('Opening edit modal for goal:', goal);

    // Safely get elements
    const titleElement = document.getElementById('goalModalTitle');
    const idElement = document.getElementById('goal-id');
    const titleInput = document.getElementById('goal-title');
    const targetInput = document.getElementById('goal-target');
    const currentInput = document.getElementById('goal-current');
    const deadlineInput = document.getElementById('goal-deadline');
    const modalElement = document.getElementById('goalModal');

    // Check if all required elements exist
    if (!titleElement || !idElement || !titleInput || !targetInput || !currentInput || !deadlineInput || !modalElement) {
        console.error('Required goal modal elements not found');
        alert('Error: Goal modal elements not found. Please refresh the page.');
        return;
    }

    // Set the values
    titleElement.textContent = 'Edit Goal';
    idElement.value = goal.id;
    titleInput.value = goal.title;
    targetInput.value = goal.target_amount;
    currentInput.value = goal.current_amount;
    deadlineInput.value = goal.deadline;

    // Show the modal
    modalElement.classList.add('show');
}

function openAddGoalModal() {
    const titleElement = document.getElementById('goalModalTitle');
    const idElement = document.getElementById('goal-id');
    const modalElement = document.getElementById('goalModal');

    if (titleElement && idElement) {
        titleElement.textContent = 'Add Goal';
        idElement.value = '';
    }

    document.getElementById('goalForm').reset();
    document.getElementById('goal-deadline').valueAsDate = new Date();

    if (modalElement) {
        modalElement.classList.add('show');
    }
}

async function handleGoalSubmit(e) {
    e.preventDefault();

    const goalId = document.getElementById('goal-id').value;
    const data = {
        title: document.getElementById('goal-title').value,
        target_amount: document.getElementById('goal-target').value,
        current_amount: document.getElementById('goal-current').value,
        deadline: document.getElementById('goal-deadline').value
    };

    try {
        const url = goalId ? `/api/goals/${goalId}` : '/api/goals';
        const method = goalId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal('goalModal');
            loadGoals();
        } else {
            console.error('Failed to save goal:', response.status);
        }
    } catch (error) {
        console.error('Error saving goal:', error);
    }
}

async function deleteGoal(id) {
    if (!confirm('Are you sure you want to delete this goal?')) return;

    try {
        const response = await fetch(`/api/goals/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadGoals();
        }
    } catch (error) {
        console.error('Error deleting goal:', error);
    }
}