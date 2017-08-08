#!/usr/bin/env python
"""
Measure rps for light requests
"""

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time


def count_rps():
    global counter
 
    while True:
        counter = 0
        time.sleep(1)
        print counter



if __name__ == "__main__":
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("localhost", 25000))

    t = Thread(target=count_rps)
    t.daemon = True
    t.start()

    while True:       
        sock.send(b"1")
        resp = sock.recv(128)
        if not resp:
            break
        counter += 1
        
