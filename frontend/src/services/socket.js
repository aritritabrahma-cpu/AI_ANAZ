let socket;

export function connectWebSocket(onMessage) {

    socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = () => {
        console.log("✅ WebSocket Connected");
        socket.send("connected");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onMessage(data);
    };

    socket.onclose = () => {
        console.log("❌ WebSocket Disconnected");

        setTimeout(() => {
            connectWebSocket(onMessage);
        }, 3000);
    };

    socket.onerror = (err) => {
        console.error(err);
    };
}