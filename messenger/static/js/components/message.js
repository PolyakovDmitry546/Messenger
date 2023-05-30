export function getMessageNode(message, channel_type='group', is_author_of_message) {
    var messageDiv = document.createElement('div');
    messageDiv.innerHTML = 
        `<div class="card ${is_author_of_message?"float-left":"float-right"} d-flex" style="max-width: 75%;">
            <div class="card-body">
                <h6 class="card-subtitle mb-2 text-body-secondary">
                    <a href="">${message.author_username}</a>
                </h6>
                <p class="card-text">${message.text}</p> 
                <p class="card-text text-end">
                    <small class="text-body-secondary ">${new Date(message.update_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</small>
                </p>
            </div>
        </div>`;

    return messageDiv;
}
