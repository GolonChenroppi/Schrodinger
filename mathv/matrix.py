import cmath
import random

import numpy as np
import itertools
import math


def get_index(index, array):
    el = array
    for i in index:
        el = el[i]
    return el


def change_index(index, array):
    el = array
    for i in index[:-1]:
        el = el[i]
    return el


def create_r_matrix(r, dim):
    matrix = np.empty([3]*dim, dtype=np.float64)
    for ii in itertools.product([0, 1, 2], repeat=dim):
        x = ii.count(0)
        y = ii.count(1)
        z = ii.count(2)
        x = r[0]**x/math.factorial(x)
        y = r[1]**y/math.factorial(y)
        z = r[2]**z/math.factorial(z)
        change_index(ii, matrix)[ii[-1]] = x*y*z
    return matrix


def amendment(c: np.ndarray, r_matrix: np.ndarray, dim):
    s = 0
    for ii in itertools.product([0, 1, 2], repeat=dim):
        s += get_index(ii, c)*get_index(ii, r_matrix)

    return s


def wave_function_raw(raw, center):
    def f(r):
        w = raw[0]
        for i in range(1, len(raw)):
            w += amendment(raw[i], create_r_matrix([r[j] - center[j] for j in range(3)], i), i)
        return w
    return f


def random_complex():
    return cmath.rect(random.uniform(0, 2), random.uniform(-cmath.pi, cmath.pi))



