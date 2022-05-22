import atexit
import subprocess
import time
import requests

address = "192.168.2.120"
isConnected = False


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
    print('ending Script')


while not isConnected:
    print("\n---pinging---\n")
    ping()
    time.sleep(3)

atexit.register(exit_handler)
