def combine_to_int(h, l):
    # clreate large integer from provided high-byte and low-byte
    res = h * 256 + l
    if res > 32767:
        res -= 65536
    return res


def conv(l, h):
    print(bin(h))
    print(bin(l))
    if not h & 0x80:
        print('positive')
        return h << 8 | l
    else:
        print('negative')
        return -((h ^ 255) << 8) | (l ^ 255) + 1


x = conv(0xa4, 0x2c) #100dps?
x = conv(0x5c, 0xc4)
print(x / 131.072)  # must be -100dps

