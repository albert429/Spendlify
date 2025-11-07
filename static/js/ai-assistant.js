// AI Chat
function handleChatKeypress(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();

    if (!question) return;

    // Add user message
    addChatMessage(question, 'user');
    input.value = '';

    // Add loading message
    const loadingId = 'loading-' + Date.now();
    addChatMessage('Thinking...', 'ai', loadingId);

    try {
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Remove loading message
        document.getElementById(loadingId)?.remove();

        // Add AI response
        addChatMessage(data.response, 'ai');

    } catch (error) {
        document.getElementById(loadingId)?.remove();
        addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}

function addChatMessage(text, type, id = null) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `chat-message ${type}`;
    if (id) div.id = id;
    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}