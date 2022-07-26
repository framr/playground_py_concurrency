#!/usr/bin/env python3
import datetime
import asyncio


def print_now():
    print(datetime.datetime.now())


async def keep_printing(name: str="") -> None:
    while True:
        print(name, end=" ")
        print_now()
        await asyncio.sleep(0.5)


async def async_main():
    try:
        await asyncio.wait_for(keep_printing("Hey"), 10)
    except asyncio.TimeoutError:
        print("oops, your time is over")


async def print3times() -> None:
    for _ in range(3):
        print_now()
        await asyncio.sleep(0.1)


async def async_main_v2() -> None:
    await keep_printing("first")
    await keep_printing("second")
    await keep_printing("third")


async def async_main_v3() -> None:
    await asyncio.gather(
        keep_printing("first"),
        keep_printing("second"),
        keep_printing("third")
        )


async def async_main_v4() -> None:
    try:
        await asyncio.wait_for(
            asyncio.gather(
                keep_printing("first"),
                keep_printing("second"),
                keep_printing("third")
            ),
            5
        )
    except asyncio.TimeoutError:
        print("oops, your time is over")


if __name__ == "__main__":


# Example: not super gracefuil timeout
#    asyncio.run(keep_printing())

# Example: graceful timeout
#    asyncio.run(async_main())

# Example:
#    coro1 = print3times()
#    coro2 = print3times()
#    asyncio.run(coro1)
#    asyncio.run(coro2)
#    # cannot reuse already used coroutine
#    asyncio.run(coro1)


# Example: only first coroutine will run here, we are in infinite loop there
#    asyncio.run(async_main_v2())

# Example: run multiple tasks using asyncio.gather!
#    asyncio.run(async_main_v3())


# Example: Combine asyncio.gather with wait_for for timeout
    asyncio.run(async_main_v4())



