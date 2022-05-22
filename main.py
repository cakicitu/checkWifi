import os
import subprocess
import atexit
#import RPi.GPIO as GPIO
import time
import webbrowser
import requests
import psutil
import socket
import nmap
import socket

address = "192.168.2.120"
isConnected = False


def callAlexaConnected():
    requests.get('https://trigger.esp8266-server.de/api/?id=541&hash=a5770e7bc8b2e5e4adcae74a3335c73d')


def remote_ips():
    '''
    Returns the list of IPs for current active connections
    '''

    remote_ips = []

    for process in psutil.process_iter():
        try:
            connections = process.connections(kind='inet')
        except psutil.AccessDenied or psutil.NoSuchProcess or OSError:
            pass
        else:
            for connection in connections:
                if connection.raddr and connection.raddr[0] not in remote_ips:
                    remote_ips.append(connection.raddr[0])

    print()
    if address in remote_ips:
        print("true")
    else:
        print("false")
    #return remote_ips

def checkNetwork():
    ip_addr = address
    scanner = nmap.PortScanner()
    host = socket.gethostbyname(ip_addr)
    scanner.scan(host, '1', '-v')
    print("IP Status: ", scanner[host].state())

def remote_ip_present(ip):
    if ip in remote_ips():
        print("true")
    else:
        print("false")



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


while True:
    print("\n---pinging---\n")
    checkNetwork()
    time.sleep(3)

# atexit.register(exit_handler)
