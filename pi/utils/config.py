# pi/utils/config.py

# WebSocket Server URI (Computer's IP and Port)
SERVER_URI = "ws://<computer_ip>:8765/signals"

# Video Streaming Server URI (WebRTC or other protocol)
VIDEO_SERVER_URI = "ws://<computer_ip>:9000"

# Flipper Zero Serial Configuration
FLIPPER_SERIAL_PORT = "/dev/ttyACM0"  # Adjust if different
FLIPPER_BAUD_RATE = 9600  # Ensure this matches Flipper Zero's settings

# Logging Configuration
LOG_FILE = "/home/pi/IQ2/pi/logs/pi.log"
