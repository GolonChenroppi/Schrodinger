from cmath import polar
from mathv.vector_operation import *


def operator_vector_multy(operator_vector):
    return lambda multi_wave, r: sum_vectors([operator_vector(wave_function, r) for wave_function in multi_wave])


def operator_scalar_multy(operator_scalar):
    return lambda multi_wave, r: sum([ operator_scalar(wave_function, r) for wave_function in multi_wave])


def density(wave_function, r):
    return polar(wave_function(r))[0]**2


def gradient(wave_function, r):
    dl = 0.0000001
    base = wave_function(r)
    p = r_dr(r, dl)
    p = [wave_function(p[i]) for i in range(3)]
    p = [(p[i] - base)*base.conjugate()/dl for i in range(3)]
    return p


def gradient_ease(wave_function, r):
    dl = 0.00001
    base = wave_function(r)
    p = r_dr(r, dl)
    p = [wave_function(p[i]) for i in range(3)]
    p = [(p[i] - base)/dl for i in range(3)]
    return p


def operator_vortex(complex_vector_operator):
    def fun(wave_function, r):
        p = complex_vector_operator(wave_function, r)
        return vp([p[i].real for i in range(3)], [p[i].imag for i in range(3)])
    return fun


def r_dr(r, dl):
    return [[r[i] + [dl, 0, 0][i] for i in range(3)],
            [r[i] + [0, dl, 0][i] for i in range(3)],
            [r[i] + [0, 0, dl][i] for i in range(3)]]


def operator_real_vector(operator_vector):
    return lambda f, r: [i.real for i in operator_vector(f, r)]


def operator_imag_vector(operator_vector):
    return lambda f, r: [i.imag for i in operator_vector(f, r)]


def get_real_vector(complex_vector):
    return [i.real for i in complex_vector]


def get_imag_vector(complex_vector):
    return [i.imag for i in complex_vector]


def operator_mod_vector(operator_vector):
    return lambda f, r: mod(operator_vector(f, r))


def operator_equality(wave_function, r):
    return 1


def operator_mul_constant(c, operator_vector):
    return lambda f, r: [c * i for i in operator_vector(f, r)]


def operator_xx(function, *operators):
    return lambda f, r: function(*[operator(f, r) for operator in operators])


def operator_r(wave_function, r):
    return r