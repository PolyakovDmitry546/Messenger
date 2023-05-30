import {getMessageNode} from './components/message.js';

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userId = JSON.parse(document.getElementById('userId').textContent);

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
    const is_author_of_message = userId==message.userId;

    document.querySelector('#chat-log').append(getMessageNode(message, "group", is_author_of_message));
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