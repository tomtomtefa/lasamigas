const socket = new WebSocket("wss://e3e8-78-126-54-178.ngrok-free.app/ws/chat/");

socket.onopen = () => {
    console.log("✅ WebSocket ouvert !");
};

socket.onmessage = (event) => {
    console.log("📩 Message reçu :", event.data);
};

socket.onerror = (error) => {
    console.log("⚠️ Erreur WebSocket :", error);
};

socket.onclose = (event) => {
    console.log("🔴 WebSocket fermé ! Rétablissement en cours...");
    setTimeout(() => {
        window.location.reload();  // Recharge la page après 3s si WebSocket est fermé
    }, 3000);
};

document.getElementById("send-button").onclick = function() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value.trim();

    if (message && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ message: message }));
        console.log("📤 Envoi du message :", message);
    } else {
        console.log("⚠️ Impossible d'envoyer, WebSocket fermé.");
    }
};
