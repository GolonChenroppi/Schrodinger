from math import cos, sin, sqrt, pi


def mod(v):
    return sqrt(sum([x**2 for x in v]))


def normalize(v):
    return [v[i]/mod(v) for i in range(3)]


def vtop(a):
    return [a[0], [a[0][i] + a[1][i] for i in range(3)]]


def ptov(a):
    return [a[0], [a[1][i] - a[0][i] for i in range(3)]]


def sp(a, b):
    return sum(a[i]*b[i] for i in range(3))


def vp(a, b):
    m = [[0, -a[2], a[1]],
         [a[2], 0, -a[0]],
         [-a[1], a[0], 0]]
    return [sum([m[y][x]*b[x] for x in range(3)])for y in range(3)]


def rotate(b, a):
    alp = mod(b)
    b = [b[i]/alp for i in range(3)]
    alp = 2*pi*alp
    L = [[b[x]*b[y] for x in range(3)]for y in range(3)]
    R = [[-b[x]*b[y] for x in range(3)]for y in range(3)]
    R[0][0] = b[1] * b[1] + b[2] * b[2]
    R[1][1] = b[0] * b[0] + b[2] * b[2]
    R[2][2] = b[0] * b[0] + b[1] * b[1]
    U = [[0, -b[2], b[1]],
         [b[2], 0, -b[0]],
         [-b[1], b[0], 0]]
    ca = cos(alp)
    sa = sin(alp)
    M = [[L[y][x] + ca*R[y][x] + sa*U[y][x] for x in range(3)] for y in range(3)]
    return [sum([M[y][i]*a[i] for i in range(3)]) for y in range(3)]


def sum_vectors(vectors):
    return [sum([vectors[j][i] for j in range(len(vectors))]) for i in range(3)]


def pri_vector(a, b):
    return [a[i] + b[i] for i in range(3)]


def power_vector(a, p):
    m = (mod(a))**(p - 1)
    return [m * i for i in a]

