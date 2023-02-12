"""
A script to test the servo, moves it through full range of motion forever
"""
import RPi.GPIO as GPIO
import time
import socket

servoPIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)

def moveToPercentagePosition(percentage):
    # 5 is zero deg, 10 is 180 deg
    p.ChangeDutyCycle(4 + (5 * percentage))

counter = 0
delta = 1
p.start(2.5) # Initialization

try:
    while True:
        moveToPercentagePosition(0)
        time.sleep(3)
        moveToPercentagePosition(1)
        time.sleep(3)
        """
        counter = counter + delta

        moveToPercentagePosition(counter / 100)

        if (counter > 100):
            delta = - 1

        if (counter < 1):
            delta = 1

        print(counter)
        time.sleep(0.1)
        """

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
