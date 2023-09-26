import {getMessageNode} from './components/message.js';

const chatLog = document.getElementById('chatLog');
const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userId = JSON.parse(document.getElementById('userId').textContent);
const chatType = document.getElementById('chatType').textContent;
var nextTopPageNumber;
var nextBottomPageNumber = 0;
var currentBottomPageNumber = 0;


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + chatType
    + '/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {  
    const message = JSON.parse(e.data);

    if (nextBottomPageNumber === currentBottomPageNumber) {
        const is_author_of_message = userId==message.author.id;
        chatLog.append(getMessageNode(message, "group", is_author_of_message));
        chatLog.scrollTop = chatLog.scrollHeight;
    }
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

async function getMessages(page) {
    var url = JSON.parse(document.getElementById('messagesURL').textContent);
    if (page !== undefined) {
        url += `?page=${page}`;
    }
    const response = await fetch(url);
    return await response.json();
}


async function showMessages() {
    const responseData = await getMessages();
    console.log(responseData);
    const messages = responseData.messages;
    for (var i in messages) {
        const is_author_of_message = (userId==messages[i].author.id);
        chatLog.append(getMessageNode(messages[i], "group", is_author_of_message));
    }
    currentBottomPageNumber = responseData.page;
    if (responseData.next_page !== null)
        nextBottomPageNumber = responseData.next_page;
}

async function addMessagesDown(page) {
    console.log('load page: ', page)
    const responseData = await getMessages(page);
    const messages = responseData.messages;
    for (var i in messages) {
        const is_author_of_message = (userId==messages[i].author.id);
        chatLog.append(getMessageNode(messages[i], "group", is_author_of_message));
    }
    currentBottomPageNumber = responseData.page;
    if (responseData.next_page !== null)
        nextBottomPageNumber = responseData.next_page;
}

var throttleTimer;
const throttle = (callback, time) => {
    if (throttleTimer) return;
    throttleTimer = true;
    setTimeout(() => {
        callback();
        throttleTimer = false;
    }, time)
}

//limit of the distance to the end of the scroll bar, crossing which the following messages are displayed
const scroollDownLimit = 250;

const handleInfiniteScroll = () => {
    throttle(() => {
        const endOfPage = chatLog.scrollHeight - chatLog.scrollTop - chatLog.clientHeight <= scroollDownLimit;
        if (endOfPage && nextBottomPageNumber !== currentBottomPageNumber) {
            addMessagesDown(nextBottomPageNumber);
        }
    }, 1000)
}

chatLog.addEventListener("scroll", handleInfiniteScroll);

showMessages();