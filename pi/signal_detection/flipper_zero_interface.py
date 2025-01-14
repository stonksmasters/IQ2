# pi/signal_detection/flipper_zero_interface.py
import serial

def detect_flipper_signals():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.write(b'READ_SIGNAL\n')
    line = ser.readline().decode('utf-8').strip()
    ser.close()
    # Parse the line as needed
    return {"signal": line}
