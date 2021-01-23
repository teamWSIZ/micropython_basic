import uasyncio as asyncio
from machine import Pin, I2C
import asi2c
import ujson

#todo: way to access I2C devices via async

i2c = I2C(scl=Pin(0),sda=Pin(2))  # software I2C
syn = Pin(5)
ack = Pin(4)
chan = asi2c.Responder(i2c, syn, ack)

async def receiver():
    sreader = asyncio.StreamReader(chan)
    while True:
        res = await sreader.readline()
        print('Received', ujson.loads(res))

async def sender():
    swriter = asyncio.StreamWriter(chan, {})
    txdata = [0, 0]
    while True:
        await swriter.awrite(''.join((ujson.dumps(txdata), '\n')))
        txdata[1] += 1
        await asyncio.sleep_ms(1500)

loop = asyncio.get_event_loop()
loop.create_task(receiver())
loop.create_task(sender())
loop.run_forever()