#!/usr/bin/env python3
"""
Simple event loop based on python generators
"""

from collections import deque


def countdown(n):
    while n > 0:
        yield n
        n -= 1

queue = deque([countdown(10), countdown(100), countdown(3)])


if __name__ == "__main__":

    while queue:
        task = queue.popleft()
        try:
            n = next(task)
            print(n)
            queue.append(task)            
        except StopIteration:
            print("Task %s finished" % task)

