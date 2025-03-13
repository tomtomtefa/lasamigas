const socket = new WebSocket("wss://be10-78-126-54-178.ngrok-free.app/ws/chat/");


chatSocket.onopen = function (event) {
    console.log("WebSocket connecté !");
};

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Message reçu :", data);
    document.querySelector("#chat-log").innerHTML += `<p>${data.message}</p>`;
};

chatSocket.onerror = function (event) {
    console.error("Erreur WebSocket :", event);
};

chatSocket.onclose = function (event) {
    console.log("WebSocket fermé :", event);
};

document.querySelector("#chat-send").onclick = function () {
    const messageInput = document.querySelector("#chat-message-input").value;
    chatSocket.send(JSON.stringify({ message: messageInput }));
};
