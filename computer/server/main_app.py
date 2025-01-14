# computer/main_app.py

import subprocess
import sys

def launch_kiosk():
    # Replace <port> with the actual port where the frontend is served
    url = "http://localhost:8000/kiosk_app/index.html"
    subprocess.Popen([
        "chromium-browser",
        "--kiosk",
        url
    ])

if __name__ == "__main__":
    launch_kiosk()
