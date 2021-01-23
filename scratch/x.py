x = 0b001
y = 0b111 ^ x

mx = (x ^ 0xff) + 1
print(mx ^ 0x80)
