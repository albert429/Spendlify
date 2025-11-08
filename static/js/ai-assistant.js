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
    
    // Format AI messages with markdown-like styling
    if (type === 'ai') {
        div.innerHTML = formatAIMessage(text);
    } else {
        div.textContent = text;
    }
    
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function formatAIMessage(text) {
    // Convert markdown-style formatting to HTML
    let formatted = text;
    
    // Convert **bold** to <strong>
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Convert bullet points (lines starting with * or •)
    const lines = formatted.split('\n');
    let inList = false;
    let result = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Check if line is a bullet point
        if (line.match(/^[\*\•\-]\s+/)) {
            if (!inList) {
                result.push('<ul>');
                inList = true;
            }
            // Remove the bullet marker and wrap in <li>
            const content = line.replace(/^[\*\•\-]\s+/, '');
            result.push(`<li>${content}</li>`);
        } else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            if (line) {
                result.push(`<p>${line}</p>`);
            }
        }
    }
    
    if (inList) {
        result.push('</ul>');
    }
    
    return result.join('');
}