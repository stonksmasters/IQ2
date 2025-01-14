// computer/kiosk_app/hud_overlay.js
const canvas = document.getElementById('hud-overlay');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Receive signal data from the server via WebSocket
const signalSocket = new WebSocket('ws://localhost:port/signals');

let signals = [];

signalSocket.onmessage = (event) => {
    signals = JSON.parse(event.data);
    drawHUD();
};

function drawHUD() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    signals.forEach(signal => {
        // Example: Draw a circle for each signal
        ctx.beginPath();
        ctx.arc(signal.x, signal.y, 10, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.closePath();
        // Add more HUD elements as needed
    });
}
