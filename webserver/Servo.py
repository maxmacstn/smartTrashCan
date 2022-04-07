import serial
import time

class Servo:
    def __init__(self):
        self.ser = serial.Serial ("/dev/ttyS4", 115200)
    
    def setAngle(self, angle):
        self.ser.write([0x73, hex(angle)])

myServo = Servo()

if __name__ == "__main__":
    while(1):
        myServo(0)
        time.sleep(2)
        myServo(90)
        time.sleep(2)
        myServo(180)
        time.sleep(2)
        

