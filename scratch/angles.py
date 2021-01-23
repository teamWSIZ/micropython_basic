from math import pi, cos, acos

for i in range(2000):
    alpha = pi * i / 1000
    v_cos = cos(alpha)
    v_alpha = acos(v_cos)
    print(f'{alpha:.3f} vs {v_alpha:.3f}')