# pi/signal_detection/flipper_zero_interface.py

import serial
import time

def detect_flipper_signals():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.write(b'READ_SIGNAL\n')  # Example command; adjust as needed
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        return {"signal": line}
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
