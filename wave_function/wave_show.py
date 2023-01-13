import cmath
import time

import pygame
import random
import multiprocessing
from mathv.vector_operation import *
from threading import Thread

distribution_methods = {'Равное'}


def points_zn_operator(h: list[float], col: int, zn, scalar_operator, wave_functon):
    return \
        [i[1] for i in sorted([
            (lambda r: [abs(scalar_operator(wave_functon, r) - zn), r])
            ([random.uniform(-h[j], h[j]) for j in range(3)])
            for j in range(100000)
        ])[0:col]
         ]


def find_points(name_points: dict):
    # name_points: {points: list[{'mod': float, 'point': list[float]], cube: list[float],
    #               'scalar_operator': scalar_operator, 'wave_function': wave_function
    #               'finding_points': Bool, 'zn': float | Complex, 'max_col': int, 'min_delta': float}
    while True:
        if name_points.get('finding_points'):
            delta = name_points['min_delta']
            r = []
            while delta >= name_points['min_delta']:
                r = [random.uniform(-name_points['cube'][j], name_points['cube'][j]) for j in range(3)]
                delta = abs(name_points['scalar_operator'](name_points['wave_function'], r) - name_points['zn'])
            name_points['points'].append({
                'mod': delta, 'point': r,
            })
            name_points['points'] = sorted(name_points['points'], key=lambda x: x['mod'])
            while len(name_points['points']) > name_points['max_col']:
                name_points['points'].pop(-1)
        else:
            time.sleep(1)


def find_vectors(name_points: dict):
    # name_points: {vectors: list[{'mod': float, 'vector': list[float]}], cube: list[float],
    #               'wave_function': wave_function, 'vector_operator': vector_operator,
    #               'finding_vectors': Bool, 'zn': float | Complex, 'max_col': int, 'min_delta': float}
    while True:
        if name_points.get('finding_vectors'):
            delta = name_points['min_delta']
            r = []
            vector = []
            while delta >= name_points['min_delta']:
                r = [random.uniform(-name_points['cube'][j], name_points['cube'][j]) for j in range(3)]
                vector = name_points['vector_operator'](name_points['wave_function'], r)
                delta = abs(mod(vector) - name_points['zn'])
            name_points['vectors'].append({
                'mod': delta, 'vector': vtop([r, vector])
            })
            name_points['vectors'] = sorted(name_points['vectors'], key=lambda x: x['mod'])
            while len(name_points['vectors']) > name_points['max_col']:
                name_points['vectors'].pop(-1)
        else:
            time.sleep(1)



# def area_min_operator(h, col, zn, complex_operator, wave):
#     return \
#         [i[1] for i in sorted([
#             (lambda r: [cmath.polar(complex_operator(wave, r) - zn)[0], r])
#             ([random.uniform(-h[j], h[j]) for j in range(3)])
#             for j in range(50000)
#         ])[0:col]
#          ]


def max_operator(h, scalar_operator, multi_wave):
    return max([scalar_operator(multi_wave, [random.uniform(-h[j], h[j]) for j in range(3)]) for i in range(10000)])


def scalar_pole_on_area(h, col, operator, func, usl=None):
    i = 0
    points = []
    while len(points) < col:
        r = [random.uniform(-h[i], h[i]) for i in range(3)]
        if usl == None or usl[0] < operator(func, r) < usl[1]:
            points.append(r)
            pygame.display.set_caption(str(len(points)))
            print(len(points))
            i = 0
        i += 1
        if i > 100000:
            print("Too mach")
            return points
    return points


def vector_pole_on_area(h, col, operator, func, usl=None, mn=1, revers=False):
    vectors, i = [], 0
    while len(vectors) < col:
        r = [random.uniform(-h[i], h[i]) for i in range(3)]
        o = operator(func, r)
        if revers:
            o = power_vector(o, -1)
        if usl == None or usl[0] < mod(o) < usl[1]:
            o = [o[i] * mn for i in range(3)]
            vectors.append(vtop([r, o]))
            i = 0
        i += 1
        if i > 100000:
            print("Too mach")
            return vectors
    return vectors


def vector_pole_on_points(points, operator, wave):
    return [(lambda p: vtop([p, operator(wave, p)]))(point) for point in points]


def finding_vector_on_points(name_dict: dict):
    pass

# def create_particles(h, col, usl, operator, multi_wave):
#     particles = []
#     while len(particles) < col:
#         r = [random.uniform(-h[i], h[i]) for i in range(3)]
#         if usl[0] < operator(multi_wave, r) < usl[1]:
#             particles.append(r)
#             print(len(particles))
#     return particles
#
#
# def move_particles(particles, operator, wave):
#     n_proc = multiprocessing.cpu_count()
#     calc = len(particles) // n_proc + 1
#     processes = []
#
#     return [move_particle(particle, operator, wave) for particle in particles]
#
#
# def move_particle(particle, operator, wave):
#     step = 0.1
#     return [particle[i] + step * operator(wave, particle)[i] for i in range(3)]
