import atexit
import subprocess
import time
import requests
import time
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

address = "192.168.2.120"
isConnected = False

#SENSOR_PIN = 23

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SENSOR_PIN, GPIO.IN)


def controllStepper():
    print("starting stepper")
    ################################
    # RPi and Motor Pre-allocations
    ################################
    #
    # define GPIO pins
    direction = 22  # Direction (DIR) GPIO Pin
    step = 23  # Step GPIO Pin
    EN_pin = 24  # enable pin (LOW to enable)

    # Declare a instance of class pass GPIO pins numbers and the motor type
    mymotortest = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
    GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output

    ###########################
    # Actual motor control
    ###########################
    #
    GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
    mymotortest.motor_go(False,  # True=Clockwise, False=Counter-Clockwise
                         "1/32",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         100,  # number of steps
                         .0005,  # step delay [sec]
                         False,  # True = print verbose output
                         .05)  # initial delay [sec]

    GPIO.cleanup()  # clear GPIO allocations after run

def mein_callback(channel):
    # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
    print('Es gab eine Bewegung!')
    takePicture()


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
    #takePicture()
    print('ending Script')
    #controllStepper()


# try:
#     print("warte auf Bewegung")
#     GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=mein_callback)
# except KeyboardInterrupt:
#     print("Beende...")
# GPIO.cleanup()
#
# while not isConnected:
#     print("\n---pinging---\n")
#     ping()
#     time.sleep(3)

controllStepper()

atexit.register(exit_handler)
