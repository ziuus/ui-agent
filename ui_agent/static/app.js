// SlovioV2 - Next Gen UI
const API_BASE = '';

const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const screenshotImg = document.getElementById('screenshotImg');
const logsPanel = document.getElementById('logsPanel');
const statusText = document.getElementById('statusText');

let pollInterval = null;

// Auto-resize textarea
chatInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send message
async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;
  
  // Add user message
  addMessage('user', text);
  chatInput.value = '';
  chatInput.style.height = 'auto';
  
  // Show typing
  setTyping(true);
  statusText.textContent = 'Processing...';
  
  try {
    const response = await fetch(`${API_BASE}/api/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: text })
    });
    
    const data = await response.json();
    addLog('Command sent: ' + text, 'success');
    
    // Poll for result
    pollForResult(text);
  } catch (error) {
    addMessage('assistant', 'Error: ' + error.message);
    setTyping(false);
    statusText.textContent = 'Error';
  }
}

// Send button
sendBtn.addEventListener('click', sendMessage);

// Enter to send
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Quick action buttons
document.querySelectorAll('.quick-action-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const cmd = btn.dataset.command;
    chatInput.value = cmd;
    sendMessage();
  });
});

// Clear button
document.getElementById('clearBtn').addEventListener('click', () => {
  chatMessages.innerHTML = '';
  addMessage('assistant', 'Chat cleared. How can I help you?');
});

// Screenshot button
document.getElementById('screenshotBtn').addEventListener('click', () => {
  fetch(`${API_BASE}/api/command`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command: 'screenshot' })
  });
});

// Poll for result
function pollForResult(userMsg) {
  let attempts = 0;
  const poll = setInterval(async () => {
    attempts++;
    try {
      const response = await fetch(`${API_BASE}/api/state`);
      const data = await response.json();
      
      // Check logs for completion
      if (data.logs && data.logs.length > 0) {
        const lastLog = data.logs[data.logs.length - 1];
        if (lastLog.message.includes('completed') || lastLog.message.includes('result:')) {
          clearInterval(poll);
          setTyping(false);
          
          // Get the response from the log
          const resultMsg = lastLog.message.replace(/^.*?: /, '');
          addMessage('assistant', resultMsg);
          statusText.textContent = 'Ready';
          
          // Update screenshot if available
          if (data.latest_screenshot_b64) {
            screenshotImg.src = `data:image/png;base64,${data.latest_screenshot_b64}`;
          }
          
          // Add logs to panel
          data.logs.forEach(log => {
            addLog(log.message, log.level === 'error' ? 'error' : 'info');
          });
        }
      }
      
      if (attempts > 30) {
        clearInterval(poll);
        setTyping(false);
        addMessage('assistant', 'Task is taking longer than expected. Check the logs for progress.');
        statusText.textContent = 'Timeout';
      }
    } catch (e) {
      console.error(e);
    }
  }, 1000);
}

// Add message to chat
function addMessage(role, content) {
  const isUser = role === 'user';
  const avatar = isUser ? '👤' : '🤖';
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  const msgDiv = document.createElement('div');
  msgDiv.className = `msg ${role}`;
  msgDiv.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-content">
      <div class="msg-bubble">${formatMessage(content)}</div>
      <div class="msg-time">${time}</div>
    </div>
  `;
  
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message with basic markdown
function formatMessage(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

// Add log entry
function addLog(message, type = 'info') {
  const entry = document.createElement('div');
  entry.className = `log-entry ${type}`;
  entry.textContent = message;
  logsPanel.appendChild(entry);
  logsPanel.scrollTop = logsPanel.scrollHeight;
}

// Typing indicator
function setTyping(show) {
  typingIndicator.classList.toggle('active', show);
}

// Initial state
addLog('UI loaded. Ready to accept commands.');
statusText.textContent = 'Ready';

// Start polling for state updates
setInterval(async () => {
  try {
    const response = await fetch(`${API_BASE}/api/state`);
    const data = await response.json();
    
    if (data.latest_screenshot_b64) {
      screenshotImg.src = `data:image/png;base64,${data.latest_screenshot_b64}`;
    }
    
    statusText.textContent = data.status === 'busy' ? 'Working...' : 'Ready';
  } catch (e) {
    // Ignore
  }
}, 3000);