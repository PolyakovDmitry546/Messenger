const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);        
    const message = JSON.parse(data.message);

    var messageDiv = document.createElement('div');
    messageDiv.innerHTML = `<a>${message.author_username}</a><p>${message.text}</p><p>${new Date(message.update_at).toString()}</p>`;
    document.querySelector('#chat-log').append(messageDiv);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': {
            'text': message
        }
    }));
    messageInputDom.value = '';
};