import subprocess
import atexit
import RPi.GPIO as GPIO
import time
import webbrowser
import requests

address = "192.168.2.120"
val = 0


def callAlexa():
    requests.get('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def controlServo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 als PWM mit 50Hz
    p.start(2.5)  # Initialisierung
    try:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def ping():
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print("ping to", address, "OK")
        controlServo()
        callAlexa()
        #global val
        #val = 1
    elif res == 2:
        print("no response from", address)
    else:
        print("ping to", address, "failed!")


def exit_handler():
    print('Device entered Network')
    # webbrowser.open('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')
    controlServo()


while val == 0:
    print("---pinging---")
    ping()

atexit.register(exit_handler)
