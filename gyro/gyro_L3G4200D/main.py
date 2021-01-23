import uasyncio as asyncio
from machine import Pin, I2C

# https://github.com/peterhinch/micropython-async/blob/master/v3/as_demos/apoll.py
GY = 0x69
REG1 = 0x20
REG4 = 0x23
STATUS_REG = 0x27

OUT_X_L = 0x28
OUT_X_H = 0x29

OUT_Y_L = 0x2A
OUT_Y_H = 0x2B
OUT_Z_L = 0x2C
OUT_Z_H = 0x2D


def nconv(l, h):
    if h & 0x80:
        hh = (h ^ 0xFF) & 0x7F
        ll = (l ^ 0xFF) + 1
        return - ((hh << 8) + ll)
    else:
        return (h << 8) + l


def get_status(status_reg_val):
    measurement_ready = not ((status_reg_val >> 3) & 1 == 0)  # reading too fast
    data_overwritten = ((status_reg_val >> 7) & 1 == 1)  # reading too slow
    return measurement_ready, data_overwritten


def select_bandwidth_and_scale(i2c):
    # Bandwidth and data-rate selection
    # 0x6F = 0b01101111
    # DR = 01 (200 Hz ODR); BW = 10 (50 Hz bandwidth); PD = 1 (parallel_component mode)
    # DR = 00 (100 Hz ODR); BW = 10 (50 Hz bandwidth); PD = 1 (parallel_component mode)
    # Zen = Yen = Xen = 1 (all axes enabled)
    i2c.writeto_mem(GY, REG1, bytes([0b00101111]))  # 00 10 1 111

    # Scale selection
    # 0x00 = 0b00000000
    # FS = 00 (+/- 250 dps full scale); (FS1,FS0) at bits (5,4) of (76543210)
    # FS = (00,01,10,11) -> (250,500,1000,2000) deg/s
    # BLE is at bit 6
    # 0b(7BFF3210) B=BLE, F=FS
    i2c.writeto_mem(GY, REG4, bytes([0b00000000]))


def read_rotations(i2c):
    g = [0] * 3
    data0 = i2c.readfrom_mem(GY, OUT_X_L, 1)  # so: little endian encoding
    data1 = i2c.readfrom_mem(GY, OUT_X_H, 1)
    g[0] = nconv(data0[0], data1[0])
    data0 = i2c.readfrom_mem(GY, OUT_Y_L, 1)
    data1 = i2c.readfrom_mem(GY, OUT_Y_H, 1)
    g[1] = nconv(data0[0], data1[0])
    data0 = i2c.readfrom_mem(GY, OUT_Z_L, 1)
    data1 = i2c.readfrom_mem(GY, OUT_Z_H, 1)
    g[2] = nconv(data0[0], data1[0])
    return g


async def update_rotation():
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    select_bandwidth_and_scale(i2c)

    # memory layout for rotation values

    scale = 32767 / 250  # = 131.072
    # scale = 114.285  # ??? this scale is used?

    # (x,y,z) == (roll,pitch,yaw)
    cnt_ready = 1
    cnt_overw = 1
    epoch = 1
    MPS = 150

    calibration_epoch = MPS * 5
    calibrated = False
    drift = [0] * 3
    angle = [0] * 3

    while True:
        try:
            status_reg_val = i2c.readfrom_mem(GY, STATUS_REG, 1)[0]
            ready, overw = get_status(status_reg_val)
            if ready:
                cnt_ready += 1  # todo: if !ready: continue
            if overw:
                cnt_overw += 1

            g = read_rotations(i2c)

            omega = [v / scale for v in g]
            # yaw += omega[2] / MPS - drift
            for i in range(3):
                angle[i] += omega[i] / MPS - drift[i]
            # subtract the drift along all axes

            if not calibrated and epoch > calibration_epoch:
                drift = [a / epoch for a in angle]  # compute drifts in all axes
                angle = [0] * 3
                print('******* calibrated; drift=', drift)
                calibrated = True

            if epoch % MPS == 0:
                print('ready:', cnt_ready, 'overwritten:', cnt_overw)
                for i in range(3):
                    print('a', i, '=', angle[i])
            epoch += 1
        except:
            print('err')

        await asyncio.sleep(1 / MPS)


async def basic_task():
    print('starting performance task')
    await asyncio.sleep(1)
    print('ending performance task')


async def main(delay):
    asyncio.run(update_rotation())  # run until complete
    await asyncio.sleep(delay)


asyncio.run(main(20))
