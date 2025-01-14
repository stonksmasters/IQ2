// computer/kiosk_app/main.js

const video = document.getElementById('live-stream');
const hudCanvas = document.getElementById('hud-overlay');
const ctx = hudCanvas.getContext('2d');

// Adjust canvas size to match video
function resizeCanvas() {
    hudCanvas.width = video.videoWidth;
    hudCanvas.height = video.videoHeight;
}

video.addEventListener('loadedmetadata', resizeCanvas);
window.addEventListener('resize', resizeCanvas);

// WebSocket for signal data
const signalSocket = new WebSocket('ws://localhost:8765');

// WebRTC setup for video streaming
let pc = new RTCPeerConnection();

pc.ontrack = function(event) {
    if (event.track.kind === 'video') {
        video.srcObject = event.streams[0];
    }
};

// Handle incoming video signaling messages
const videoSignalingSocket = new WebSocket('ws://localhost:9000');

videoSignalingSocket.onmessage = async function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'offer') {
        await pc.setRemoteDescription(new RTCSessionDescription(data));
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        videoSignalingSocket.send(JSON.stringify({
            type: pc.localDescription.type,
            sdp: pc.localDescription.sdp
        }));
    }
};

// Create an offer (for testing purposes; in production, signaling should be handled properly)
async function createOffer() {
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    videoSignalingSocket.send(JSON.stringify({
        type: pc.localDescription.type,
        sdp: pc.localDescription.sdp
    }));
}

createOffer();

// Store received signals
let signals = [];

// Handle incoming signal data
signalSocket.onmessage = (event) => {
    signals = JSON.parse(event.data);
    drawHUD();
};

// Controls for signal tracking
const trackBluetooth = document.getElementById('track-bluetooth');
const trackWifi = document.getElementById('track-wifi');
const trackFlipper = document.getElementById('track-flipper');

trackBluetooth.addEventListener('change', drawHUD);
trackWifi.addEventListener('change', drawHUD);
trackFlipper.addEventListener('change', drawHUD);

// Function to draw HUD overlay
function drawHUD() {
    ctx.clearRect(0, 0, hudCanvas.width, hudCanvas.height);
    if (signals.bluetooth && trackBluetooth.checked) {
        signals.bluetooth.forEach(signal => {
            drawSignal(signal, 'blue');
        });
    }
    if (signals.wifi && trackWifi.checked) {
        signals.wifi.forEach(signal => {
            drawSignal(signal, 'green');
        });
    }
    if (signals.flipper && trackFlipper.checked) {
        signals.flipper.forEach(signal => {
            drawSignal(signal, 'red');
        });
    }
}

// Function to draw individual signals
function drawSignal(signal, color) {
    // Example: Assuming signal has x and y coordinates normalized between 0 and 1
    const x = signal.x * hudCanvas.width;
    const y = signal.y * hudCanvas.height;
    ctx.beginPath();
    ctx.arc(x, y, 15, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}
