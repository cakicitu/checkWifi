import atexit
import subprocess
import time
import requests
import time
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

address = "192.168.2.120"
isConnected = False

SENSOR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)


def mein_callback(channel):
    # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
    print('Es gab eine Bewegung!')
    takePicture()


try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=mein_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Beende...")
GPIO.cleanup()

def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()


def callAlexaConnected():
    requests.get('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def callAlexaDisconnected():
    requests.get('https://trigger.esp8266-server.de/api/?id=542&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def ping():
    global isConnected
    res = subprocess.call(['ping', '-c', '5', address])
    print("res: ", res)
    if res == 0:
        print("ping to", address, "OK")
        if not isConnected:
            callAlexaConnected()
            isConnected = True
    elif res == 2:
        print("no response from", address)
        if isConnected:
            callAlexaDisconnected()
            isConnected = False
    else:
        print("ping to", address, "failed!")
        if isConnected:
            callAlexaDisconnected()
            isConnected = False


def exit_handler():
    takePicture()
    print('ending Script')

while not isConnected:
    print("\n---pinging---\n")
    ping()
    time.sleep(3)


atexit.register(exit_handler)
