import serial, time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

while True:
    if arduino.in_waiting:
        line = arduino.readline().decode().strip()
        print(line)
