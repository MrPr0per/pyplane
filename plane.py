import pygame
import math
import numpy as np
from enum import Enum, auto


class Plane:
    def __init__(self, sc: pygame.Surface, scale=100, dx=0, dy=0):
        self.sc = sc  # пайгеймовская поверхность, на которой будет отрисовываться картинка
        self.sc_width, self.sc_height = sc.get_width(), sc.get_height()
        self.scale = scale  # пикселей на еденицу плоскости
        self.scale_speed = 1.1  # во сколько раз изменяется масштаб за один шаг колесиком мыши
        self.center = [self.sc_width / 2 - dx * scale,
                       self.sc_height / 2 - dy * scale]  # координаты начала координат на sc [px]
        self.n_mul = 0  # количество уможений line_scale на 5 (для корректной нумерации сетки)
        self.line_scale = self.scale  # пикселей на расстояние между линиями сетки в еденицах плоскости
        while True:
            if self.line_scale < 20:
                self.line_scale *= 5
                self.n_mul += 1
            elif self.line_scale > self.sc_height / 2:
                self.line_scale /= 5
                self.n_mul -= 1
            else:
                break
        self.font_size = max(20, int(self.sc_height / 40))
        self.font = pygame.font.Font(None, self.font_size)

    def process_events(self, events, keys):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                no_move_point_sc = pygame.mouse.get_pos()
                no_move_point_crd = self.convet_to_plane_crd(no_move_point_sc)

                if event.button == 4:
                    self.scale *= self.scale_speed
                    self.line_scale *= self.scale_speed
                if event.button == 5:
                    self.scale /= self.scale_speed
                    self.line_scale /= self.scale_speed

                no_move_point_crd_2 = self.convet_to_plane_crd(no_move_point_sc)

                self.center[0] = self.center[0] - (no_move_point_crd[0] - no_move_point_crd_2[0]) * self.scale
                self.center[1] = self.center[1] + (no_move_point_crd[1] - no_move_point_crd_2[1]) * self.scale

        # перетаскивание мышкой
        delta = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0] and keys[pygame.K_SPACE]:
            self.center[0] = self.center[0] + delta[0]
            self.center[1] = self.center[1] + delta[1]

        # корректировка масштаба линий сетки
        if self.line_scale < 20:
            self.line_scale *= 5
            self.n_mul += 1
        if self.line_scale > self.sc_height / 2:
            self.line_scale /= 5
            self.n_mul -= 1

    def draw_grid(self, line_scale, color='#555555'):
        i = self.center[0] % line_scale
        while i < self.sc_width:
            pygame.draw.line(self.sc, color, (i, 0), (i, self.sc_height))
            i += line_scale
        i = self.center[1] % line_scale
        while i < self.sc_width:
            pygame.draw.line(self.sc, color, (0, i), (self.sc_width, i))
            i += line_scale

    def draw_cross(self, color='#ffffff'):
        pygame.draw.line(self.sc, color, (0, self.center[1]), (self.sc_width, self.center[1]), 1)
        pygame.draw.line(self.sc, color, (self.center[0], self.sc_height), (self.center[0], 0), 1)

    def draw_numbers(self):
        # отрисовка значений
        n_units = 5 ** self.n_mul
        text_plus1 = self.font.render(str(n_units), True, '#777777')
        text_0 = self.font.render(str(0), True, '#777777')
        text_minus1 = self.font.render(str(-n_units), True, '#777777')

        x_m1, y_m1 = self.convet_to_sc_crd((-n_units, -n_units))
        x_0, y_0 = self.convet_to_sc_crd((0, 0))
        x_p1, y_p1 = self.convet_to_sc_crd((n_units, n_units))

        self.sc.blit(text_plus1, (x_p1 + 5, y_0 + 5))
        self.sc.blit(text_plus1, (x_0 + 5, y_p1 + 5))
        self.sc.blit(text_minus1, (x_m1 + 5, y_0 + 5))
        self.sc.blit(text_minus1, (x_0 + 5, y_m1 + 5))
        self.sc.blit(text_0, (x_0 + 5, y_0 + 5))

    def draw(self, without_numbers=False):
        self.sc.fill('#000000')

        if self.n_mul > 0:
            self.draw_grid(self.line_scale / 5, color='#222222')  # отрисовываем неяркую сетку поменьше
        self.draw_grid(self.line_scale)
        self.draw_cross()
        if not without_numbers:
            self.draw_numbers()

    def convet_to_sc_crd(self, crd):
        """ковертирует координату точки на плоскости в координату соответсвующего пикселя на экране"""
        return [crd[0] * self.scale + self.center[0], -1 * crd[1] * self.scale + self.center[1]]

    def convert_plane_x_to_sc(self, x):
        """ковертирует значение x точки на плоскости в значение x соответсвующего пикселя на экране"""
        return x * self.scale + self.center[0]

    def convert_plane_y_to_sc(self, y):
        """ковертирует значение y точки на плоскости в значение y соответсвующего пикселя на экране"""
        return -1 * y * self.scale + self.center[1]

    def convert_pl_d_to_sc(self, d):
        """ковертирует расстояние на плоскости в расстояние на экране"""
        return d * self.scale

    def convet_to_plane_crd(self, crd):
        """ковертирует координату пикселя на экране в координату соответсвующей точки на плоскости"""
        return [(crd[0] - self.center[0]) / self.scale, (self.center[1] - crd[1]) / self.scale]
