def bbin(x, len=16):
    return bin(x)[2:].zfill(len)


def zbin(x, n):
    r = ''
    for i in range(n):
        r = str(x % 2) + r
        x >>= 1
    return r


def conv(l, h):
    if not h & 0x80:
        return h << 8 | l  # is positive
    else:
        return -((h ^ 255) << 8) | (l ^ 255) + 1


def nconv(l, h):
    if h & 0x80:
        hh = (h ^ 0xFF) & 0x7F
        ll = (l ^ 0xFF) + 1
        return - ((hh << 8) + ll)
    else:
        return (h << 8) + l


# 100dps
l = 0xA4
h = 0x2C

# 200dps
l = 0x49
h = 0x59

x = (h << 8) + l
# print(bbin(h<<8))
# print(bbin(l))
# print(bbin(x))
# print(x / 131)

# high 200dps
print(bbin(0x59, 8))
print(bbin(0xA6, 8))
print(bbin((0xA6 ^ 0xFF), 8))  # conversion to absolute

print('--')
# low 200dps
print(bbin(0x49, 8))
print(bbin(0xb7, 8))
print(bbin((0xb7 ^ 0xff) + 1, 8))  # conversion to absolute

print('---total---')
val_pos = (0x59 << 8) + 0x49
val_neg = (((0xA6 ^ 0xFF) & 0x7F) << 8) + (0xB7 ^ 0xFF + 1)
print(val_pos)
print(val_neg)

print('---conv')
print(conv(0x49, 0x59))
print(conv(0xB7, 0xA6))
print('---nconv')
print(nconv(0x49, 0x59))
print(nconv(0xB7, 0xA6))

scale = 131.068
scale = 114.285  # ??? this scale is used?
omega = nconv(0x49, 0x59) / scale
print(omega)
