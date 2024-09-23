const roomName = JSON.parse(document.getElementById("course").textContent)

const chatSocket = new WebSocket(
    "ws://" +
    window.location.host +
    "/ws/chat/" +
    roomName +
    "/"
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    var chatDiv = document.getElementById("chat");

    if (JSON.parse(document.getElementById("user").textContent) === data.user) {
        chatDiv.innerHTML += `<div class="d-flex flex-row justify-content-end mb-4">
          <div class="p-3 me-3 border bg-body-tertiary" style="border-radius: 15px;">
            <p class="small mb-0">${data.message}</p>
          </div>
          <span>${data.user}</span>
        </div>`;
    }
    else {
        chatDiv.innerHTML += `<div class="d-flex flex-row justify-content-start mb-4">
              <span>${data.user}</span>
              <div class="p-3 ms-3 bg-primary text-white" style="border-radius: 15px;">
                <p class="small mb-0">${data.message}</p>
              </div>
            </div>`;
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
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
