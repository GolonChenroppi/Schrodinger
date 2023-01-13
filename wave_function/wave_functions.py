import cmath
from math import pi, sqrt, sin, cos, exp
import math
from mathv.vector_operation import *


def dec_to_sph(rd):
    x, y, z = rd[0], rd[1], rd[2]
    a = math.atan2(y, x)
    r = math.hypot(x, y)
    b = math.atan2(r, z)
    r = math.hypot(z, r)
    return [r, b, a]


quantum_numbers = [[[f'{n} {l} {m}'
                     for m in range(-l, l + 1)]
                    for l in range(-1, n)]
                   for n in [1, 2, 3]]

hydrogen_functions = {}
for n in quantum_numbers:
    for l in n:
        for m in l:
            hydrogen_functions.update({m: None})


def wave_200(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return cmath.rect(1 / 4 / sqrt(2 * pi) * (2 - r) * exp(-r / 2), 0)


hydrogen_functions['2 0 0'] = wave_200


def wave_211(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return 10*cmath.rect(1 / 8 / sqrt(pi) * r * exp(-r / 2) * sin(b), a)


hydrogen_functions['2 1 1'] = wave_211


def wave_210(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return cmath.rect(1 / 4 / sqrt(2 * pi) * r * exp(-r / 2) * cos(b), 0)


hydrogen_functions['2 1 0'] = wave_210


def wave_21n1(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return cmath.rect(1 / 8 / sqrt(pi) * r * exp(-r / 2) * sin(b), -a)


hydrogen_functions['2 1 -1'] = wave_21n1


def wave_322(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return r ** 2 / 162 / sqrt(pi) * exp(-r / 3) * sin(b) ** 2 * cmath.exp(2j * a)


hydrogen_functions['3 2 2'] = wave_322


def wave_321(rd):
    rs = dec_to_sph(rd)
    r, b, a = rs[0], rs[1], rs[2]
    o = 1
    return r ** 2 / 81 / sqrt(pi) * exp(-r / 3) * sin(b) * cos(b) * cmath.exp(1j * a)


hydrogen_functions['3 2 1'] = wave_321


def wave_space(density):
    return lambda rd: sqrt(density)


hydrogen_functions.update({'const': wave_space})


def wave_flow(density, k):
    return lambda rd: cmath.rect(sqrt(density), sp(rd, k))


hydrogen_functions.update({'flow': wave_flow})

key_del = []
for key in hydrogen_functions:
    if hydrogen_functions[key] is None:
        key_del.append(key)
[hydrogen_functions.pop(i) for i in key_del]


