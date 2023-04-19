// Connect to the WebSocket server
const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/');

// Handle incoming messages
chatSocket.onmessage = function(event) {
    const message = event.data;
    // Display the message in the message container
    const messagesContainer = document.querySelector('#messages');
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    messagesContainer.appendChild(messageElement);
};

// Send messages when the form is submitted
document.querySelector('#chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
});
