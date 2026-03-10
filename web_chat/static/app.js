const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const messageInput = document.getElementById('message');
const clearBtn = document.getElementById('clear-btn');

function addMessage(role, text) {
  const el = document.createElement('div');
  el.className = `message ${role}`;
  el.textContent = `${role === 'user' ? 'You' : 'Assistant'}: ${text}`;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

addMessage('assistant', 'Hello! I can help with basic questions, small code, summaries, and planning.');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage('user', message);
  messageInput.value = '';

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  const data = await response.json();
  if (!response.ok) {
    addMessage('assistant', data.error || 'Something went wrong.');
    return;
  }

  addMessage('assistant', data.reply);
});

clearBtn.addEventListener('click', async () => {
  await fetch('/api/clear', { method: 'POST' });
  chat.innerHTML = '';
  addMessage('assistant', 'Chat cleared.');
});
