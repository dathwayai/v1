"use strict";

const textMessage = document.getElementById('chat_text');
const sendMessageBtn = document.getElementById('send_chat');
const chatBody = document.querySelector('chatBody');


sendMessageBtn.addEventListener("click", function () {
    console.log("clicked");
    const textMessageValue = textMessage.value;
    console.log(textMessageValue)
    if (textMessageValue.trim() !== '') {
        chatBody.appendChild(messageEl(textMessageValue, "user_message"))
        // Simulate bot typing
        appendTypingAnimation();

        $.ajax({
            url: 'chat',
            method: 'POST',
            data: { 'text': textMessageValue },
            success: function (response) {
                // Remove typing animation
                removeTypingAnimation();
                if (response.message === 'success') {
                    // Display bot's response
                    appendMessage('received', response.bot_response);
                } else {
                    console.log("Unexpected response:", response);
                }
            },
            error: function (xhr, status, error) {
                removeTypingAnimation();
                console.log("Error:", status, error);
            }
        });
    }
});

const messageEl = (message, className) => {
    const chatEl = document.createElement("div");
    chatEl.classList.add("chat", `${className}`);
    let chatContent =
        className === "chat-bot"
            ? `<div class="messages-detail__body-item-container">
                    <div class="">
                        <i class='bx bxs-user-circle' ></i>
                    </div>
                    
                    <div class="messages-detail__body-item-text">
                            <p>${message}</p> 
                    </div>
                </div>`:`<div class="messages-detail__body-item-container">
                    <div class="messages-detail__body-item-text">
                        <p>${message}</p>
                </div>
                <div class="">
                    <i class='bx bxs-bot'></i>
                </div>
                
                </div>`;
        chatEl.innerHTML = chatContent;
        return chatEl;

}

function appendMessage(type, message) {
    const messageClass = type === 'sent' ? 'sent-message' : 'received-message';
    const messageElement = document.createElement('div');
    messageElement.className = messageClass;
    messageElement.innerHTML = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop(chatBody.scrollHeight);
}

function appendTypingAnimation() {
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    chatBody.appendChild(typingIndicator);
    chatBody.scrollTop(chatBody.scrollHeight);
}

function removeTypingAnimation() {
    $('.typing-indicator').remove();
}
