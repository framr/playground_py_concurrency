#!/usr/bin/env python3
from re import S
from typing import Callable, Coroutine
import asyncio
import time

import httpx


async def crawl0(
    prefix: str, url: str = ""
) -> None:
    url = url or prefix
    print(f"crawling {url}")
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            await crawl0(prefix, line)


todo = set()
addr = "https://langa.pl/crawl/"
async def progress(
    url: str,
    algo: Callable[..., Coroutine]
) -> None:
    asyncio.create_task(
        algo(url),
        name=url
    )
    todo.add(url)
    start = time.time()
    while todo:
        print(f"{len(todo)}: " + ", ".join(sorted(todo))[-38:])
        await asyncio.sleep(0.5)
    end = time.time()
    print(f"Took {int(end - start)} sec")


async def crawl1(
    prefix: str, url: str = ""
) -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            todo.add(line)
            await crawl1(prefix, line)
    todo.discard(url)



async def crawl2(
    prefix: str, url: str = ""
) -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            todo.add(line)
            asyncio.create_task(
                crawl2(prefix, line),
                name=line
            )
    todo.discard(url)



async def crawl3(
    prefix: str, url: str = ""
) -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            task = asyncio.create_task(
                crawl3(prefix, line),
                name=line
            )
            todo.add(task)


async def progress2(
    url: str,
    algo: Callable[..., Coroutine]
) -> None:
    task = asyncio.create_task(
        algo(url),
        name=url
    )
    todo.add(task)
    start = time.time()
    while todo:
        done, _pending = await asyncio.wait(todo, timeout=0.5)
        todo.difference_update(done)
        urls = (t.get_name() for t in todo)
        print(f"{len(todo)}: " + ", ".join(sorted(urls))[-75:])
        await asyncio.sleep(0.5)
    end = time.time()
    print(f"Took {int(end - start)} sec")


async def async_main() -> None:
    try:
        await progress2(addr, crawl3)
    except asyncio.CancelledError:
        for task in todo:
            task.cancel()
        done, pending = await asyncio.wait(todo, timeout=1.0)
        todo.difference_update(done)
        todo.difference_update(pending)
        if todo:
            print("warning: new tasks added while we were canceling")



if __name__ == "__main__":


# Example
# Problems:
# - Reporting progress should be done not by task itself
# - Recursive calls is bad
# - No concurrency
# - Better to use context manager
#    asyncio.run(crawl0("https://langa.pl/crawl"))


# Example: Still no concurrency
#    asyncio.run(progress(addr, crawl1))

# Example:
#    asyncio.run(progress(addr, crawl2))

# Example:
#    asyncio.run(progress2(addr, crawl3))

    loop = asyncio.get_event_loop()
    task = loop.create_task(async_main())
    loop.call_later(10, task.cancel)
    loop.run_until_complete(task)
