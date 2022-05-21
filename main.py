import subprocess
import atexit
import RPi.GPIO as GPIO
import time

address = "192.168.2.120"
val = 0


def controlServo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 als PWM mit 50Hz
    p.start(2.5)  # Initialisierung
    try:
        while True:
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(12.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            time.sleep(0.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def ping():
    res = subprocess.call(['ping', '-c', '1', address])
    if res == 0:
        print("ping to", address, "OK")
        global val
        val = 1
    elif res == 2:
        print("no response from", address)
    else:
        print("ping to", address, "failed!")


def exit_handler():
    print('Device entered Network')
    controlServo()


while val == 0:
    print("---pinging---")
    ping()

atexit.register(exit_handler)
