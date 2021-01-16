import uasyncio as asyncio
from machine import Pin


async def drive_local_led():
    led = Pin(2, Pin.OUT)
    on = True
    while True:
        if on:
            led.off()
        else:
            led.on()
        on = not on
        await asyncio.sleep(0.5)


async def fast_tics_to_console():
    while True:
        await asyncio.sleep(0.05)
        print('tick')


async def main():
    print('Zaczynamy pracę...')
    asyncio.create_task(fast_tics_to_console())  # just a task
    asyncio.run(drive_local_led())  # run until complete


asyncio.run(main())
