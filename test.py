import asyncio
import time
from threading import Thread

main_loop = asyncio.new_event_loop()


def g():
    global main_loop
    for i in range(4):
        main_loop.create_task(e())


async def e():
    await asyncio.sleep(1)
    print('erferferferf')



async def main():
    for i in range(10):
        if i == 2:
            Thread(target=g, args=()).run()
        await asyncio.sleep(1)
        print('wed')

main_loop.run_until_complete(main())

