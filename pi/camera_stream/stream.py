from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import threading
import time
import sys

app = Flask(__name__)

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()

# Shared variable for the latest frame
latest_frame = None
lock = threading.Lock()

def capture_frames():
    global latest_frame
    while True:
        try:
            # Capture frame as a numpy array
            frame = picam2.capture_array()

            # Add timestamp overlay (optional)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Encode the frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                with lock:
                    latest_frame = jpeg.tobytes()

            # Display the frame locally
            cv2.imshow('Live Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Control frame rate (e.g., ~30 FPS)
            time.sleep(1/30)
        except KeyboardInterrupt:
            break

    # Clean up
    picam2.stop()
    cv2.destroyAllWindows()
    sys.exit()

def generate():
    global latest_frame
    while True:
        with lock:
            if latest_frame is None:
                continue
            frame = latest_frame

        # Yield frame in byte format as part of the MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Simple HTML page to display the video stream
    return '''
    <html>
    <head>
        <title>Raspberry Pi Camera Stream</title>
    </head>
    <body>
        <h1>Raspberry Pi Camera Stream</h1>
        <img src="/video_feed" width="640" height="480">
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Start frame capture in a separate thread
    t = threading.Thread(target=capture_frames)
    t.daemon = True
    t.start()

    # Run Flask app
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    except KeyboardInterrupt:
        pass
