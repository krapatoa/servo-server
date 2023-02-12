"""
Server that controls the servo position, go to <ip>:8080 for the main input page,
<ip>:8080/duty/<num> to set the angle to a number between 0 and 100
"""

import RPi.GPIO as GPIO
import time
from flask import Flask, request, abort
import os

servoPIN = 32
percentage = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)

id = 0

def moveToPercentagePosition(newPercentage):
    # 5 is zero deg, 10 is 180 deg
    global percentage
    percentage = newPercentage
    duty = 2 + ((percentage * (55 - 15) / 100 + 15)/10)
    p.ChangeDutyCycle(duty)


p.start(2.5) # Initialization
moveToPercentagePosition(0)

app = Flask(__name__)

@app.route('/duty/<int:duty>')
def setduty(duty):
    moveToPercentagePosition(duty)
    return ''

@app.route('/dutyseq/<int:seq>/<int:duty>')
def setdutyseq(seq, duty):
    global id
    if seq >= id:
        moveToPercentagePosition(duty)
        id = id + 1
    return f'{id}'

@app.route('/getduty')
def getduty():
    global duty
    return f'{int(percentage)}'

@app.route('/')
def mainpage():
    print("Loaded main page!")
    fd = os.open("main.html", os.O_RDONLY)
    fileData = os.read(fd, 10000).decode()
    os.close(fd)
    return fileData

@app.route('/v2')
def v2():
    print("Loaded v2 page!")
    fd = os.open("v2.html", os.O_RDONLY)
    fileData = os.read(fd, 10000).decode()
    os.close(fd)
    return fileData

@app.route('/v3')
def v3():
    print("Loaded v3 page!")
    fd = os.open("v3.html", os.O_RDONLY)
    fileData = os.read(fd, 10000).decode()
    os.close(fd)
    return fileData

app.run(host='0.0.0.0', port=8080, debug=False, threaded=False)


#except KeyboardInterrupt:
p.stop()
GPIO.cleanup()
