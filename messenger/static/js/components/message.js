export function getMessageNode(message, channel_type='group', is_author_of_message) {
    var messageDiv = document.createElement('div');
    const dateOptions = { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" };
    const messageDate =  new Date(message.update_at).toLocaleTimeString([], dateOptions);
    messageDiv.innerHTML = 
        `<div class="d-flex ${is_author_of_message?"justify-content-start":"justify-content-end"}">
            <div class="card" style="max-width: 70%; min-width: 30%;">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-body-secondary">
                        <a href="">${message.author.username}</a>
                    </h6>
                    <p class="card-text">${message.text}</p> 
                    <p class="card-text text-end">
                        <small class="text-body-secondary ">${messageDate}</small>
                    </p>
                </div>
            </div>
        </div>`;

    return messageDiv;
}
