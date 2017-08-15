#!/usr/bin/env python3
# fib microservice   :)

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket, socketpair
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor as Pool
from collections import deque
from select import select

from fib import fib
pool = Pool(4)


tasks = deque()
waiters_recv = {}
waiters_send = {}
waiters_future = {}


future_notify, future_event = socketpair()
def future_done(future):
    tasks.append(waiters_future.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield "recv", future_event
        future_event.recv(128)

tasks.append(future_monitor())

def run(tasks):

    while any([tasks, waiters_recv, waiters_send]):

        # wait for i/o
        while not tasks:
            can_recv, can_send, _ = select(waiters_recv, waiters_send, [])
            for s in can_recv:
                tasks.append(waiters_recv.pop(s))
            for s in can_send:
                tasks.append(waiters_send.pop(s))

        # process tasks
        task = tasks.popleft()
        try:
            why, who = next(task)
            if why == "recv":
                waiters_recv[who] = task
            elif why == "send":
                waiters_send[who] = task
            elif why == "future":
                waiters_future[who] = task
                who.add_done_callback(future_done)

            else:
                raise ValueError("wrong task type, should be recv or send")

        except StopIteration:
            print("task done")


def fib_handler(client):
    
    while True:
        yield 'recv', client 
        value = client.recv(128)
        if not value:
            break

        future = pool.submit(fib, int(value))
        result = future.result()
        yield "future", future        
        resp = str(result).encode('utf-8') + b'\n'
        yield 'send', client
        client.send(resp)

    print("handler closed")


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
        
    while True:
        yield 'recv', sock
        client, addr = sock.accept()
        print("connection", addr)
        #Thread(target=fib_handler, args=(client,)).start()
        
        tasks.append(
            fib_handler(client)
        )


if __name__ == '__main__':

    tasks.append(fib_server(('', 25000)))
    run(tasks)



