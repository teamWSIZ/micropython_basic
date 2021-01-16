import uasyncio as asyncio
from machine import Pin, I2C


# https://github.com/peterhinch/micropython-async/blob/master/v3/as_demos/apoll.py


def combine_register_values(h, l):
    # if not h[0] & 0x80:
    #     return h[0] << 8 | l[0]
    # return -((h[0] ^ 255) << 8) | (l[0] ^ 255) + 1

    res = h * 256 + l
    if res > 32767:
        res -= 65536
    return res


def decode_status(status_reg_val):
    not_measured_yet = ((status_reg_val >> 3) & 1 == 0)  # reading too fast
    data_overwritten = ((status_reg_val >> 7) & 1 == 1)  # reading too slow
    return not_measured_yet, data_overwritten


async def update_rotation():
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    REG4 = 0x23
    REG1 = 0x20
    ADDR = 0x69  # from i2c.scan() = ; good for L3G4200D

    # 0x6F = 0b01101111
    # DR = 01 (200 Hz ODR); BW = 10 (50 Hz bandwidth); PD = 1 (normal mode)
    # Zen = Yen = Xen = 1 (all axes enabled)
    i2c.writeto_mem(ADDR, REG1, bytes([0b01101111]))  # 01 10 1 111

    # 0x00 = 0b00000000
    # FS = 00 (+/- 250 dps full scale); (FS1,FS0) at bits (5,4) of (76543210)
    # FS = (00,01,10,11) -> (250,500,1000,2000) deg/s
    i2c.writeto_mem(ADDR, REG4, bytes([0b00000000]))

    # memory layout for rotation values
    OUT_X_L = 0x28
    OUT_X_H = 0x29
    OUT_Y_L = 0x2A
    OUT_Y_H = 0x2B
    OUT_Z_L = 0x2C
    OUT_Z_H = 0x2D

    STATUS_REG = 0x27
    scale = 32768 / 250  # = 131.072

    # (x,y,z) == (roll,pitch,yaw)
    ready = 1
    overw = 1
    mx = 0
    yaw = 0
    epoch = 0
    MPS = 20
    while True:
        try:
            status_reg_val = i2c.readfrom_mem(ADDR, STATUS_REG, 1)[0]
            status = decode_status(status_reg_val)
            if status[0]:
                ready += 1  # todo: if !ready: continue
            if status[1]:
                overw += 1
            g = [0] * 3
            data0 = i2c.readfrom_mem(ADDR, OUT_X_L, 1)
            data1 = i2c.readfrom_mem(ADDR, OUT_X_H, 1)
            g[0] = combine_register_values(data1[0], data0[0])
            data0 = i2c.readfrom_mem(ADDR, OUT_Y_L, 1)
            data1 = i2c.readfrom_mem(ADDR, OUT_Y_H, 1)
            g[1] = combine_register_values(data1[0], data0[0])
            data0 = i2c.readfrom_mem(ADDR, OUT_Z_L, 1)
            data1 = i2c.readfrom_mem(ADDR, OUT_Z_H, 1)
            g[2] = combine_register_values(data1[0], data0[0])
            omega = [v / scale for v in g]
            for o in omega:
                mx = max(mx, abs(o))
            if epoch > 2:
                print('angular velocities:', omega)
                print('ready:', ready, 'overwritten:', overw, 'ratio:', ready / overw, 'max_omega:', mx, 'yaw:', yaw)
                epoch = 0
            epoch += 1
            yaw += omega[2] / MPS
            # yaw -= 0.09 / MPS
        except:
            print('err')

        await asyncio.sleep(1 / MPS)


async def basic_task():
    print('starting performance task')
    await asyncio.sleep(1)
    print('ending performance task')


async def main(delay):
    # asyncio.create_task(temp_update())  # just a task
    asyncio.run(update_rotation())  # run until complete
    # asyncio.run(ticks())
    await asyncio.sleep(delay)
    # program finish; return to prompt


asyncio.run(main(20))
