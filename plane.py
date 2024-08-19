import pygame
import math
import numpy as np
from enum import Enum, auto


# TODO: отображение цифр по всей длине
# TODO: отображение цифр даже если оси за пределами экрана

class Plane:
    def __init__(self, sc: pygame.Surface, scale=100, dx=0, dy=0):
        self.sc = sc  # пайгеймовская поверхность, на которой будет отрисовываться картинка
        self.sc_width, self.sc_height = sc.get_width(), sc.get_height()
        self.scale_speed = 1.1  # во сколько раз изменяется масштаб за один шаг колесиком мыши
        self.scale_deg = np.array(
            [int(math.log(scale, self.scale_speed))] * 2,  # сколько раз увеличивался масштаб по каждой из осей
            dtype=int)
        self.center = np.array([self.sc_width / 2 - dx * scale,
                                self.sc_height / 2 - dy * scale])  # координаты начала координат на sc [px]

        self.grid_base = 10  # во сколько раз увеличивается/уменьшается минимальное деление сетки
        min_grid_gap = 50
        self.max_grid_gap = min_grid_gap * self.grid_base

        # TODO: умножение не на 10, а *5 *2 *5 *2 *5 ... + 2 мелкие сетки на 0.2|0.5 и на 0.1

        self.font_size = max(20, int(self.sc_height / 40))
        self.font = pygame.font.Font(None, self.font_size)

        self.color_of_background = [0] * 3
        self.color_of_cross = [255] * 3
        self.color_of_main_grid = [75] * 3
        self.color_of_small_grid = [25] * 3

    def scale(self, dimetion: int = None):
        """количество пикселей на еденицу плоскости"""
        if dimetion is None:
            if np.all(self.scale_deg == self.scale_deg[0]):
                dimetion = 0
            else:
                raise ValueError(f'сетка имеет разный масштаб по разным осям: {self.scale_deg=}, '
                                 f'так что нужно явно указать нужное измерение')

        return self.scale_speed ** self.scale_deg[dimetion]

    def grid_division(self, dimetion: int = None):
        """минимальное деление главной сетки (в еденицах площади)"""
        # https://www.desmos.com/calculator/hmlu3lqpyp
        return self.grid_base ** (
            - math.floor(
                math.log(
                    self.scale(dimetion) / self.max_grid_gap,
                    self.grid_base
                ) + 1)
        )

    def grid_gap(self, dimention: int = None):
        """кол-во пикселей между линиями главной сетки"""
        return self.scale(dimention) * self.grid_division(dimention)

    def process_events(self, events, keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                no_move_point_sc = pygame.mouse.get_pos()
                no_move_point_crd = self.convet_to_plane_crd(no_move_point_sc)

                degree_delta = 0
                if event.button == pygame.BUTTON_WHEELUP:
                    degree_delta = 1
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    degree_delta = -1

                shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

                if not shift_pressed and not ctrl_pressed:
                    self.scale_deg += degree_delta
                if shift_pressed:
                    self.scale_deg[0] += degree_delta
                if ctrl_pressed:
                    self.scale_deg[1] += degree_delta

                if shift_pressed and event.button == pygame.BUTTON_MIDDLE:
                    self.scale_deg[0] = self.scale_deg[1]
                if ctrl_pressed and event.button == pygame.BUTTON_MIDDLE:
                    self.scale_deg[1] = self.scale_deg[0]

                no_move_point_crd_2 = self.convet_to_plane_crd(no_move_point_sc)

                # TODO: переписать на векторы
                self.center[0] = self.center[0] - (no_move_point_crd[0] - no_move_point_crd_2[0]) * self.scale(0)
                self.center[1] = self.center[1] + (no_move_point_crd[1] - no_move_point_crd_2[1]) * self.scale(1)

        # TODO: переписать на векторы
        # перетаскивание мышкой
        delta = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            self.center[0] = self.center[0] + delta[0]
            self.center[1] = self.center[1] + delta[1]

    def draw(self, without_numbers=False):
        self.sc.fill(self.color_of_background)

        self.draw_grid((self.grid_division(0) / self.grid_base, self.grid_division(1) / self.grid_base),
                       self.color_of_small_grid)
        self.draw_grid((self.grid_division(0), self.grid_division(1)), self.color_of_main_grid)
        self.draw_cross()
        # if not without_numbers:
        #     self.draw_numbers()

    def draw_grid(self, grid_division: tuple[float, float], color):
        grid_gap = (grid_division[0] * self.scale(0), grid_division[1] * self.scale(1))
        i = self.center[0] % grid_gap[0]
        while i < self.sc_width:
            pygame.draw.line(self.sc, color, (i, 0), (i, self.sc_height))
            i += grid_gap[0]
        i = self.center[1] % grid_gap[1]
        while i < self.sc_width:
            pygame.draw.line(self.sc, color, (0, i), (self.sc_width, i))
            i += grid_gap[1]

    def draw_cross(self):
        pygame.draw.line(self.sc, self.color_of_cross, (0, self.center[1]), (self.sc_width, self.center[1]), 1)
        pygame.draw.line(self.sc, self.color_of_cross, (self.center[0], self.sc_height), (self.center[0], 0), 1)

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

    def convet_to_sc_crd(self, crd):
        """ковертирует координату точки на плоскости в координату соответсвующего пикселя на экране"""
        # return [crd[0] * self.scale() + self.center[0], -1 * crd[1] * self.scale() + self.center[1]]
        return self.convert_plane_x_to_sc(crd[0]), self.convert_plane_y_to_sc(crd[1])

    def convert_plane_x_to_sc(self, x):
        """ковертирует значение x точки на плоскости в значение x соответсвующего пикселя на экране"""
        return x * self.scale(0) + self.center[0]

    def convert_plane_y_to_sc(self, y):
        """ковертирует значение y точки на плоскости в значение y соответсвующего пикселя на экране"""
        return -1 * y * self.scale(1) + self.center[1]

    def convert_pl_d_to_sc(self, d):
        """ковертирует расстояние на плоскости в расстояние на экране"""
        return d * self.scale()

    def convet_to_plane_crd(self, crd):
        """ковертирует координату пикселя на экране в координату соответсвующей точки на плоскости"""
        return [
            (crd[0] - self.center[0]) / self.scale(0),
            (self.center[1] - crd[1]) / self.scale(1)
        ]
