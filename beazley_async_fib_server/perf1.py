#!/usr/bin/env python
"""
Measure response time for heavy request 
"""

import time

from socket import socket, AF_INET, SOCK_STREAM



if __name__ == "__main__":

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 25000))


    while True:
 
        start = time.time()       
        sock.send(b'30')
        resp = sock.recv(128)
        if not resp:
            break

        print (time.time() - start)
    
