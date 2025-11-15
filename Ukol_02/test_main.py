import serial
import time

# Nastav správný port podle svého systému
# Např. "COM3" ve Windows, nebo "/dev/ttyACM0" na Linuxu
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)

time.sleep(2)  # počkej, až se Arduino inicializuje

while True:
    cmd = input("Zadej 1 (rozsvítit) nebo 0 (zhasnout), q pro konec: ")

    if cmd == 'q':
        break
    elif cmd in ['0', '1']:
        arduino.write(cmd.encode())
    else:
        print("Neplatný příkaz")

arduino.close()
