from math import cos, sin, sqrt, pi
from mathv.vector_operation import *
import pygame


class Camera:
    def __init__(self, scene: pygame.Surface, bg_color):
        self.video = None
        self.scene = scene
        self.position = [-20, 3, 3]
        self.a = 0
        self.asp = 0.02
        self.b = 0
        self.sp = 0.1
        self.gips = False
        self.m = [[0 for x in range(3)] for y in range(3)]
        n = pi * 11 / 12
        self.n1 = [[cos(n), -sin(n)],
                   [sin(n), cos(n)]]
        self.n2 = [[cos(n), sin(n)],
                   [-sin(n), cos(n)]]
        self.vsor = [cos(self.b) * cos(self.a), cos(self.b) * sin(self.a), sin(self.b)]
        self.screen_size = self.scene.get_size()
        self.obsor_x = 0.5
        self.obsor_y = self.obsor_x * self.screen_size[1] / self.screen_size[0]
        self.color = [255, 255, 255]
        self.bg_color = bg_color
        self.focus = [0, 0, 0]

    def set_matrix(self):
        m1 = [[0 for x in range(3)] for y in range(3)]
        m1[0][0] = cos(self.a)
        m1[1][0] = -sin(self.a)
        m1[0][1] = sin(self.a)
        m1[1][1] = cos(self.a)
        m1[2][2] = 1

        m2 = [[0 for x in range(3)] for y in range(3)]
        m2[0][0] = cos(self.b)
        m2[2][0] = -sin(self.b)
        m2[0][2] = sin(self.b)
        m2[2][2] = cos(self.b)
        m2[1][1] = 1

        self.m = [[sum([m2[y][i] * m1[i][x] for i in range(3)]) for x in range(3)] for y in range(3)]
        self.mxp = [sum([self.m[y][x] * self.position[x] for x in range(3)]) for y in range(3)]

    def rend_point2(self, point):
        op = [sum([self.m[y][i] * point[i] for i in range(3)]) - self.mxp[y] for y in range(3)]
        if op[0] > 0:
            op = [op[i] / op[0] / 2 for i in range(3)]
            t = [round((-op[1] + self.obsor_x) * self.screen_size[0]),
                 round((-op[2] + self.obsor_y) * self.screen_size[0])]
            pygame.draw.circle(self.scene, self.color, [t[0], t[1]], 1)

    def rend_vector(self, vector):
        t = [0, 0]
        out = True
        for k, point in enumerate(vector):
            op = [point[i] - self.position[i] for i in range(3)]
            op = [sum([self.m[y][i] * op[i] for i in range(3)]) for y in range(3)]
            if op[0] > 0:
                op = [op[i] / op[0] / 2 for i in range(3)]
                t[k] = [round((-op[1] + self.obsor_x) * self.screen_size[0]),
                        round((-op[2] + self.obsor_y) * self.screen_size[0])]
            else:
                out = False
        if out:
            pygame.draw.line(self.scene, self.color, t[0], t[1], 1)
            l = [t[1][i] - t[0][i] for i in range(2)]
            if mod(l) > 0:
                l = [l[i] / mod(l) * 10 for i in range(2)]
                t[0] = [round(sum([l[x] * self.n1[y][x] for x in range(2)])) for y in range(2)]
                p = [t[1][x] + t[0][x] for x in range(2)]
                pygame.draw.line(self.scene, self.color, t[1], p, 1)

                t[0] = [round(sum([l[x] * self.n2[y][x] for x in range(2)])) for y in range(2)]
                p = [t[1][x] + t[0][x] for x in range(2)]
                pygame.draw.line(self.scene, self.color, t[1], p, 1)

    def rend_vector_pole(self, vectors, color):
        self.color = color
        for vector in vectors:
            self.rend_vector(vector)

    def rend_scalar_pole(self, points, color):
        self.color = color
        for point in points:
            self.rend_point2(point)

    def rend_xyz(self):
        self.color = [255, 0, 0]
        self.rend_vector([[0, 0, 0], [1, 0, 0]])
        self.color = [0, 255, 0]
        self.rend_vector([[0, 0, 0], [0, 1, 0]])
        self.color = [0, 0, 255]
        self.rend_vector([[0, 0, 0], [0, 0, 1]])

    def clear(self):
        pygame.display.flip()
        self.scene.fill(self.bg_color)

    def key_step(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.a += self.asp
        if keystate[pygame.K_RIGHT]:
            self.a -= self.asp
        if keystate[pygame.K_UP]:
            self.b += self.asp
            if self.b > pi / 2:
                self.b = pi / 2
        if keystate[pygame.K_DOWN]:
            self.b -= self.asp
            if self.b < -pi / 2:
                self.b = -pi / 2
        if keystate[pygame.K_a]:
            for i in range(3):
                self.position[i] += [-sin(self.a), cos(self.a), 0][i] * self.sp
        if keystate[pygame.K_d]:
            for i in range(3):
                self.position[i] += [+sin(self.a), -cos(self.a), 0][i] * self.sp
        if keystate[pygame.K_w]:
            for i in range(3):
                self.position[i] += [cos(self.a), sin(self.a), 0][i] * self.sp
        if keystate[pygame.K_s]:
            for i in range(3):
                self.position[i] += [-cos(self.a), -sin(self.a), 0][i] * self.sp
        if keystate[pygame.K_SPACE]:
            self.position[2] += self.sp
        if keystate[pygame.K_LSHIFT]:
            self.position[2] -= self.sp
        self.sp = 0.1
        self.gips = False
        if keystate[pygame.K_LCTRL]:
            self.sp = 1
            self.gips = True

    def focus_position(self):
        b = [cos(self.b) * cos(self.a), cos(self.b) * sin(self.a), sin(self.b)]
        L = [[b[x] * b[y] for x in range(3)] for y in range(3)]
        self.position = [sum([L[x][y]*self.position[y] for y in range(3)])for x in range(3)]

##    def start_video(self, name):
##        self.video = Video(self.screen_size, name)
##
##    def frame_rend_point(self, point):
##        op = [sum([self.m[y][i] * point[i] for i in range(3)]) - self.mxp[y] for y in range(3)]
##        if op[0] > 0:
##            op = [op[i] / op[0] / 2 for i in range(3)]
##            t = [round((-op[1] + self.obsor_x) * self.screen_size[0]),
##                 round((-op[2] + self.obsor_y) * self.screen_size[0])]
##            if 0 <= t[0] < self.screen_size[0] and 0 <= t[1] < self.screen_size[1]:
##                self.video.draw_point(t[0], t[1], self.color)
##
##    def save_frame(self):
##        self.video.save_frame()
##        self.video.clear()
##
##    def end_video(self):
##        self.video.release()

