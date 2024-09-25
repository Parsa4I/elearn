const roomName = JSON.parse(document.getElementById("course").textContent);
const currentUser = JSON.parse(document.getElementById("user").textContent);

const chatSocket = new WebSocket(
    "ws://" +
    window.location.host +
    "/ws/chat/" +
    roomName +
    "/"
);

function addMessage(user, message) {
    var chatDiv = document.getElementById("chat");
    if (currentUser === user) {
        chatDiv.innerHTML += `<div class="d-flex flex-row justify-content-end mb-4">
        <div class="p-3 me-3 border bg-body-tertiary" style="border-radius: 15px;">
          <p class="small mb-0">${message}</p>
        </div>
        <span>${user}</span>
      </div>`;
    }
    else {
        chatDiv.innerHTML += `<div class="d-flex flex-row justify-content-start mb-4">
              <span>${user}</span>
              <div class="p-3 ms-3 bg-primary text-white" style="border-radius: 15px;">
                <p class="small mb-0">${message}</p>
              </div>
            </div>`;
    }
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    addMessage(data.user, data.message);
}

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.getElementById("messageArea").focus();

document.getElementById("messageArea").onkeyup = function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        document.getElementById("send-btn").click();
    }
};

document.getElementById("send-btn").onclick = function (e) {
    const messageInput = document.getElementById("messageArea");
    const message = messageInput.value;

    const isWhitespaceString = str => !str.replace(/\s/g, '').length

    if (!isWhitespaceString(message)) {
        chatSocket.send(JSON.stringify({
            "message": message
        }));
        messageInput.value = "";
    }
};

const messagesUrl = "http://" +
    window.location.host +
    "/chat/" +
    roomName +
    "/messages/";

fetch(messagesUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        data.forEach(element => {
            addMessage(element.user, element.body);
            console.log(element.user);
            console.log(element.body);
        });
    });
