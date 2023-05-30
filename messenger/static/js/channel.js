import {getMessageNode} from './components/message.js';

async function getMessages() {
    const url = JSON.parse(document.getElementById('messagesURL').textContent);
    const response = await fetch(url);
    return await response.json();
}

async function showMessages() {
    const userId = JSON.parse(document.getElementById('userId').textContent);
    const messages = JSON.parse(await getMessages());
    const chatLog = document.querySelector('#chat-log')
    for (var i in messages) {
        const is_author_of_message = (userId==messages[i].author_id);
        chatLog.append(getMessageNode(messages[i], "group", is_author_of_message));
    }
}

showMessages();