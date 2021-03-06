import utime
from machine import Pin
import machine, onewire, ds18x20, time
# https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/
import uasyncio as asyncio
import utime as time


# https://github.com/peterhinch/micropython-async/blob/master/v3/as_demos/apoll.py


def sens_id(barray):
    # generate 0--1007 sensor id hash; should be unique, and readable
    w = [_ for _ in barray]
    res = 1
    modulo = 1007
    for _ in w:
        res = (res * _) % modulo + 37
    return res % modulo


async def temp_update():
    ds_pin = machine.Pin(4)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    roms = ds_sensor.scan()
    print('Found DS devices (thermometers): ')
    for r in roms:
        print('sensor:', sens_id(r))

    while True:
        ds_sensor.convert_temp()
        await asyncio.sleep(1.0)
        for rom in roms:
            temp = ds_sensor.read_temp(rom)
            sensor_id = sens_id(rom)
            print('sensor', sensor_id, ' ', temp)
        await asyncio.sleep(5)


async def main(delay):
    print('Test runs for 20s.')
    asyncio.run(temp_update())  # run until complete
    await asyncio.sleep(delay)


asyncio.run(main(20))
