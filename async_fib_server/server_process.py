#!/usr/bin/env python3
# fib microservice   :)

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket 
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

from fib import fib


pool = Pool(4)

def fib_handler(client):
    
    while True:
        value = client.recv(128)
        if not value:
            break

        future = pool.submit(fib, int(value))
        result = future.result()
        
        resp = str(result).encode('utf-8') + b'\n'
        client.send(resp)

    print("handler closed")


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    
    while True:
        client, addr = sock.accept()
        print("connection", addr)
        Thread(target=fib_handler, args=(client,)).start()
 

if __name__ == '__main__':

    fib_server(('', 25000))
