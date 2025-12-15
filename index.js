// document.getElementById('get').addEventListener('click', async () => {
//     const response = await fetch('http://localhost:3000/');
//     const data = await response.text();
//     document.getElementById('result').innerText = data;
// });

const msgs = document.getElementById('messages');
const input = document.getElementById('chat-input');
const btn = document.getElementById('get');
const typing = document.getElementById('typing');

function addMsg(text, isUser) {
    const div = document.createElement('div');
    div.className = `msg ${isUser ? 'user' : 'bot'}`;
    div.innerHTML = `
                <div class="avatar">${isUser ? 'U' : 'S'}</div>
                <div class="bubble">${text}</div>
            `;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

async function send() {
    const text = input.value.trim();
    if (!text) return;

    addMsg(text, true);
    input.value = '';
    btn.disabled = true;
    typing.classList.add('show');

    

    getBotResponse(text);
}

btn.onclick = send;
input.onkeypress = (e) => {
    if (e.key === 'Enter') send();
};

input.focus();

async function getBotResponse(message) {
    try {
        // Show typing indicator
        typing.classList.add('show');
        btn.disabled = true;
        console.log("User message:", message);

        // Fetch response from backend
        const response = await fetch('http://localhost:3000/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });
        const data = await response.json();

        const data1 = marked.parse(data);

        console.log("Bot response:", data1);

        // Hide typing indicator
        typing.classList.remove('show');

        // Add real bot message
        addMsg(data, false);

    } catch (error) {
        typing.classList.remove('show');
        addMsg("Uh-oh. Something broke. Try again 😬", false);
        console.error(error);
    } finally {
        btn.disabled = false;
        input.focus();
    }
}