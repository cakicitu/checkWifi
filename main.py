import subprocess
import atexit
import RPi.GPIO as GPIO
import time
import webbrowser
import requests

address = "192.168.2.120"
isConnected = False


def callAlexa():
    requests.get('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def controlServo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 als PWM mit 50Hz
    p.start(2.5)  # Initialisierung
    p.ChangeDutyCycle(12.5)
    p.stop()
    GPIO.cleanup()


def ping():
    global isConnected
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print("ping to", address, "OK")
        if not isConnected:
            controlServo()
            callAlexa()
            isConnected = True
    elif res == 2:
        print("no response from", address)
        isConnected = True
    else:
        print("ping to", address, "failed!")
        isConnected = True


def exit_handler():
    print('ending Script')
    # webbrowser.open('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')
    # controlServo()


while not isConnected:
    print("---pinging---")
    ping()

atexit.register(exit_handler)
