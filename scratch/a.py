from tt import do_it

do_it('abc')

counter = 0
g = 0
while True:
    counter += 1
    IPS = 10 ** 7
    if counter % IPS == 0:
        print(f'tick {g}')
        g += 1
        counter = 0
