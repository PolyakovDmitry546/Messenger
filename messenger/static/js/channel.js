import {getMessageNode} from './components/message.js';

const chatLog = document.getElementById('chatLog');
const userId = JSON.parse(document.getElementById('userId').textContent);
var nextTopPageNumber;
var nextBottomPageNumber;
var currentBottomPageNumber;

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