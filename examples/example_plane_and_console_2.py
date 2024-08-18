import math
import pygame
import time
from plane import Plane
from console import Console


# фигуры Лиссажу
# особенности работы с плоскостью и консолью выделены восклицательным знаком (!)


def draw_lissajous_curve(pl: Plane, freq: tuple[int, int], offset=0.0):
    points = []
    for i in range(360):
        rad = i / 180 * math.pi
        x = math.cos(rad * freq[0] + offset)
        y = math.sin(rad * freq[1])
        points.append((x, y))

    sc_points = [pl.convet_to_sc_crd(p) for p in points]
    pygame.draw.lines(pl.sc, (0, 255, 0), True, sc_points)
    # pygame.draw.circle(pl.sc, (255, 0, 0), sc_points[0], 100)


def main():
    # стандартная инициализация пугейма
    pygame.init()
    sc = pygame.display.set_mode((1200, 700))
    FPS = 120
    clock = pygame.time.Clock()

    # !нужно создать объект плоскости и консоли
    pl = Plane(sc)
    console = Console()

    t0 = time.time()
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # закрытие окна на ESC
                    pygame.quit()
                    quit()

        # !раз в кадр нужно вызвать обработчик евентов и отрисовщик
        pl.process_events(events, keys)
        pl.draw()

        # теперь отрисовываем свои штуки
        t = time.time() - t0
        draw_lissajous_curve(pl, (2, 3), t)

        # !сверху отрисовываем консоль
        console.draw_lines(sc, [
            f'{pl.scale(0)=}',
            f'{pl.scale(1)=}',
            f'{pl.scale_deg=}',
        ])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
