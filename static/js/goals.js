async function loadGoals() {
    try {
        const response = await fetch('/api/goals');
        if (!response.ok) {
            throw new Error('Failed to load goals');
        }
        goals = await response.json();
        renderGoals();
    } catch (error) {
        console.error('Error loading goals:', error);
        const container = document.getElementById('goals-list');
        if (container) {
            container.innerHTML = '<div class="empty-state"><div class="icon">⚠️</div><p>Error loading goals</p></div>';
        }
    }
}

function renderGoals() {
    const container = document.getElementById('goals-list');

    if (!container) {
        console.error('Goals container not found');
        return;
    }

    if (!goals || goals.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="icon">🎯</div><p>No goals yet. Start setting your financial targets!</p></div>';
        return;
    }

    // Sort goals by deadline
    const sortedGoals = [...goals].sort((a, b) => {
        return new Date(a.deadline) - new Date(b.deadline);
    });

    container.innerHTML = sortedGoals.map(goal => {
        const progress = Math.min((goal.current_amount / goal.target_amount) * 100, 100);
        const goalJson = JSON.stringify(goal).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        const remaining = Math.max(0, goal.target_amount - goal.current_amount);

        // Calculate days until deadline
        const today = new Date();
        const deadline = new Date(goal.deadline);
        const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

        let urgentClass = '';
        if (goal.status === 'completed') {
            urgentClass = 'completed';
        } else if (daysLeft < 30) {
            urgentClass = 'urgent';
        }

        return `
            <div class="goal-card ${urgentClass}">
                <div class="goal-header">
                    <div class="goal-title-section">
                        <div class="goal-title">${goal.title || 'Untitled Goal'}</div>
                        <div class="goal-target">Target: $${parseFloat(goal.target_amount || 0).toFixed(2)}</div>
                    </div>
                    <span class="goal-status-badge ${goal.status || 'active'}">${goal.status || 'active'}</span>
                </div>
                
                <div class="goal-progress">
                    <div class="progress-info">
                        <div class="progress-labels">
                            <span class="progress-amount">$${parseFloat(goal.current_amount || 0).toFixed(2)}</span>
                            <span class="progress-target">of $${parseFloat(goal.target_amount || 0).toFixed(2)}</span>
                        </div>
                        <span class="progress-percentage">${progress.toFixed(1)}%</span>
                    </div>
                    <div class="enhanced-progress-bar">
                        <div class="enhanced-progress-fill" style="width: ${progress}%"></div>
                    </div>
                    <div class="progress-milestones">
                        <div class="milestone">0%</div>
                        <div class="milestone">25%</div>
                        <div class="milestone">50%</div>
                        <div class="milestone">75%</div>
                        <div class="milestone">100%</div>
                    </div>
                </div>
                
                <div style="margin: 15px 0; padding-top: 15px; border-top: 1px solid #e9ecef;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9em; color: #6c757d;">
                        <span>📅 Deadline: ${goal.deadline}</span>
                        ${goal.status !== 'completed' ? `<span>💰 Remaining: $${remaining.toFixed(2)}</span>` : '<span>✅ Completed!</span>'}
                    </div>
                    ${daysLeft > 0 && goal.status !== 'completed' ? `
                        <div style="margin-top: 5px; font-size: 0.85em; color: ${daysLeft < 30 ? '#dc3545' : '#28a745'};">
                            ${daysLeft} days left
                        </div>
                    ` : ''}
                </div>
                
                <div class="goal-actions">
                    <button class="btn btn-sm btn-edit" onclick='openEditGoalModal(${goalJson})'>Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteGoal('${goal.id}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function openEditGoalModal(goal) {
    console.log('Opening edit modal for goal:', goal);

    const modal = document.getElementById('goalModal');
    const title = document.getElementById('goalModalTitle');

    if (!modal || !title) {
        console.error('Goal modal elements not found');
        alert('Error: Goal modal not found. Please refresh the page.');
        return;
    }

    // Set the values
    title.textContent = 'Edit Goal';

    const fields = {
        'goal-id': goal.id,
        'goal-title': goal.title,
        'goal-target': goal.target_amount,
        'goal-current': goal.current_amount,
        'goal-deadline': goal.deadline
    };

    for (const [id, value] of Object.entries(fields)) {
        const element = document.getElementById(id);
        if (element) {
            element.value = value || '';
        } else {
            console.warn(`Element ${id} not found`);
        }
    }

    // Show the modal
    modal.classList.add('show');
}

function openAddGoalModal() {
    const modal = document.getElementById('goalModal');
    const title = document.getElementById('goalModalTitle');
    const form = document.getElementById('goalForm');
    const idField = document.getElementById('goal-id');

    if (!modal || !title || !form || !idField) {
        console.error('Goal modal elements not found');
        alert('Error: Modal elements not found. Please refresh the page.');
        return;
    }

    title.textContent = 'Add Goal';
    idField.value = '';
    form.reset();

    // Set today as default deadline
    const today = new Date();
    today.setDate(today.getDate() + 30); // Default to 30 days from now
    document.getElementById('goal-deadline').valueAsDate = today;
    document.getElementById('goal-current').value = '0';

    modal.classList.add('show');
}

async function handleGoalSubmit(e) {
    e.preventDefault();

    const goalId = document.getElementById('goal-id').value;
    const data = {
        title: document.getElementById('goal-title').value.trim(),
        target_amount: parseFloat(document.getElementById('goal-target').value),
        current_amount: parseFloat(document.getElementById('goal-current').value),
        deadline: document.getElementById('goal-deadline').value
    };

    // Validation
    if (!data.title) {
        alert('Please enter a goal title');
        return;
    }

    if (!data.target_amount || data.target_amount <= 0) {
        alert('Please enter a valid target amount');
        return;
    }

    if (data.current_amount < 0) {
        alert('Current amount cannot be negative');
        return;
    }

    if (data.current_amount > data.target_amount) {
        if (!confirm('Current amount exceeds target. This goal will be marked as completed. Continue?')) {
            return;
        }
    }

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
            await loadGoals();
            alert(goalId ? 'Goal updated successfully!' : 'Goal added successfully!');
        } else {
            const error = await response.json();
            alert('Error saving goal: ' + (error.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving goal:', error);
        alert('Error saving goal. Please try again.');
    }
}

async function deleteGoal(id) {
    if (!confirm('Are you sure you want to delete this goal?')) return;

    try {
        const response = await fetch(`/api/goals/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await loadGoals();
            alert('Goal deleted successfully!');
        } else {
            alert('Error deleting goal');
        }
    } catch (error) {
        console.error('Error deleting goal:', error);
        alert('Error deleting goal. Please try again.');
    }
}