import struct

z = 0b1101001  # one byte, =105
print(z)  # normalny int
print(hex(z))  # 0x69
print(bin(z))  # 0b1101001

# for larger ints -- combining into a signle one can be tricky
# ba = b'\x00\x01'
# iba = int.from_bytes(ba, 'big')
# print(ba)
# print(iba)  # 1
# iba = int.from_bytes(ba, 'little')
# print(iba)  # 256

# creating a byte array:
intlist = [1, 15]
print(bytes(intlist))  # b'\x01\x0f'
