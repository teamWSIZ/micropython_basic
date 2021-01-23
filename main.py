import uasyncio as asyncio
from machine import Pin, I2C
from bmp280 import BMP280


async def update_pressure():
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    bmp = BMP280(i2c)

    print(bmp.temperature)
    print(bmp.pressure)
    last10 = []
    epoch = 0

    while True:
        baro = bmp.pressure
        last10.append(baro)
        if len(last10) > 10:
            last10 = last10[1:]
            suma = sum(last10)
            if epoch % 100 == 0:
                print('baro_avg=', suma / 10)
                print('temp=', bmp.temperature)
        epoch += 1
        await asyncio.sleep(0.1)


async def main():
    asyncio.run(update_pressure())  # run until complete


asyncio.run(main())
