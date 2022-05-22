import subprocess
import atexit
import RPi.GPIO as GPIO
import time
import webbrowser
import requests

address = "192.168.2.120"
isConnected = False


def callAlexaConnected():
    requests.get('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def callAlexaDisconnected():
    requests.get('https://trigger.esp8266-server.de/api/?id=542&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


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
    res = subprocess.call(['ping', '-c', '5', address])
    print("res: ", res)
    if res == 0:
        print("ping to", address, "OK")
        if not isConnected:
            controlServo()
            callAlexaConnected()
            isConnected = True
    elif res == 2:
        print("no response from", address)
        callAlexaDisconnected()
        isConnected = False
    else:
        print("ping to", address, "failed!")
        callAlexaDisconnected()
        isConnected = False


def exit_handler():
    print('ending Script')
    # webbrowser.open('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')
    # controlServo()


while True:
    print("\n---pinging---\n")
    ping()

# atexit.register(exit_handler)
