const socket = new WebSocket("wss://be10-78-126-54-178.ngrok-free.app/ws/chat/");

socket.onopen = function () {
    console.log("WebSocket connecté !");
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Message reçu :", data);

    let chatLog = document.querySelector("#chat-box");
    if (chatLog) {
        chatLog.innerHTML += `<p>${data.message}</p>`;
    } else {
        console.error("Élément #chat-box introuvable !");
    }
};

socket.onerror = function (event) {
    console.error("Erreur WebSocket :", event);
};

socket.onclose = function (event) {
    console.log("WebSocket fermé :", event);
};

document.addEventListener("DOMContentLoaded", function () {
    let sendButton = document.querySelector("#chat-send");
    let messageInput = document.querySelector("#message-input");

    if (sendButton && messageInput) {
        sendButton.onclick = function () {
            const message = messageInput.value;
            socket.send(JSON.stringify({ message: message }));
        };
    } else {
        console.error("Bouton ou champ message introuvable !");
    }
});
