import math
import pygame
import time
from _plane_v4 import Plane


# для примера сделаю вращение земли вокруг солнца
# особенности работы с плоскостью выделены восклицательным знаком (!)
# управление:
#   у плоскости:
#       перемещаться по плоскости с помощью перетаскивания зажатой ЛКМ
#       менять масштаб на колесико
#   у этой симуляции:
#       плобел - пауза

def draw_solar_system():
    t = time.time() - t0
    if is_time_stoped:
        t = stoped_time - t0

    if is_sun_static:
        sun_center = (0, 0)
    else:
        sun_center = (1000000 + 5000000 * t, 1000000 + 0.25 * 50000 * t)
    earth_center = (sun_center[0] +  math.cos(t * k_time / (365 * 24 * 60 * 60) * 2 * math.pi) * d_from_sun_to_earth,
                    sun_center[1] +  math.sin(t * k_time / (365 * 24 * 60 * 60) * 2 * math.pi) * d_from_sun_to_earth)
    mars_center = (sun_center[0] +   math.cos(t * k_time / (687 * 24 * 60 * 60) * 2 * math.pi) * d_from_sun_to_mars,
                   sun_center[1] +   math.sin(t * k_time / (687 * 24 * 60 * 60) * 2 * math.pi) * d_from_sun_to_mars)
    moon_center = (earth_center[0] + math.cos(t * k_time / (31 * 24 * 60 * 60) * 2 * math.pi) * d_from_earth_to_moon,
                   earth_center[1] + math.sin(t * k_time / (31 * 24 * 60 * 60) * 2 * math.pi) * d_from_earth_to_moon)

    sc.blit(font.render('Sun', True, '#00ff00'),
            pl.convet_to_sc_crd((sun_center[0] + sun_radius, sun_center[1] + sun_radius)))
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(sun_center), pl.convert_pl_d_to_sc(sun_radius), 3)
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(sun_center), pl.convert_pl_d_to_sc(d_from_sun_to_earth), 1)
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(sun_center), pl.convert_pl_d_to_sc(d_from_sun_to_mars), 1)

    sc.blit(font.render('Earth', True, '#00ff00'),
            pl.convet_to_sc_crd((earth_center[0] + earth_radius, earth_center[1] + earth_radius)))
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(earth_center), pl.convert_pl_d_to_sc(earth_radius), 3)
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(earth_center), pl.convert_pl_d_to_sc(d_from_earth_to_moon),
                       1)

    sc.blit(font.render('Moon', True, '#00ff00'),
            pl.convet_to_sc_crd((moon_center[0] + moon_radius, moon_center[1] + moon_radius)))
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(moon_center), pl.convert_pl_d_to_sc(moon_radius), 3)

    sc.blit(font.render('Mars', True, '#00ff00'),
            pl.convet_to_sc_crd((mars_center[0] + mars_radius, mars_center[1] + mars_radius)))
    pygame.draw.circle(sc, (0, 255, 0), pl.convet_to_sc_crd(mars_center), pl.convert_pl_d_to_sc(mars_radius), 3)

    # двигаем камеру:
    if focus_on == 'Earth':
        pl.center[0] = pl.convert_plane_x_to_sc(0) - pl.convert_plane_x_to_sc(earth_center[0]) + pl.sc_width / 2
        pl.center[1] = pl.convert_plane_y_to_sc(0) - pl.convert_plane_y_to_sc(earth_center[1]) + pl.sc_height / 2
        # pl.center[0] = pl.convert_plane_x_to_sc(sun_center[0]) - pl.convert_plane_x_to_sc(
        #     earth_center[0]) + pl.sc_width / 2
        # pl.center[1] = pl.convert_plane_y_to_sc(sun_center[1]) - pl.convert_plane_y_to_sc(
        #     earth_center[1]) + pl.sc_height / 2
    elif focus_on == 'Moon':
        pl.center[0] = pl.convert_plane_x_to_sc(sun_center[0]) - pl.convert_plane_x_to_sc(
            moon_center[0]) + pl.sc_width / 2
        pl.center[1] = pl.convert_plane_y_to_sc(sun_center[1]) - pl.convert_plane_y_to_sc(
            moon_center[1]) + pl.sc_height / 2
    elif focus_on == 'Mars':
        pl.center[0] = pl.convert_plane_x_to_sc(sun_center[0]) - pl.convert_plane_x_to_sc(
            mars_center[0]) + pl.sc_width / 2
        pl.center[1] = pl.convert_plane_y_to_sc(sun_center[1]) - pl.convert_plane_y_to_sc(
            mars_center[1]) + pl.sc_height / 2


# стандартная инициализация пугейма
pygame.init()
sc = pygame.display.set_mode((1200, 700))
pygame.display.set_caption('test plane_v3')
FPS = 120
clock = pygame.time.Clock()

# !нужно создать объект плоскости
pl = Plane(sc, 1 / 10_000)

# параметры (можно менять)
# focus_on = 'Earth'  # на каом объекте сфокусироваться (нестабильно при близком масшабе)
focus_on = None
is_sun_static = True  # статично ли солнце
k_time = (60 * 60 * 24) * 2  # во сколько раз в симуляции ускорено время (при k_time = 60 * 60 * 24   1 сек = 1 день)

# системные переменные и константы (нельзя менять)
t0 = time.time()  # вреемя начала симуляции
is_time_stoped = False  # остановилось ли время
stoped_time = 0  # на каком значении остановилось время
font_size = 20
font = pygame.font.Font(None, font_size)
# 1 клетка поля = 1 км
sun_radius = 696_340
earth_radius = 6_371
moon_radius = 1_737
mars_radius = 3_389
d_from_sun_to_earth = 147_000_000
d_from_sun_to_mars = 228_000_000
d_from_earth_to_moon = 384_400
while True:
    # нужно сохранить pygame.event.get() в отдельную переменную,
    # тк иначе не будет работать управление плоскостью,
    # (потому что если 2 раза за кадр вызывать pygame.event.get(),
    # то оно вернет события только в первый раз, а во второй - пустоту)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            print(pygame.QUIT)
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # закрытие окна на ESC
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                if not is_time_stoped:
                    is_time_stoped = True
                    stoped_time = time.time()
                else:
                    is_time_stoped = False
                    t0 = t0 + (time.time() - stoped_time)

    # !раз в кадр нужно вызвать обработчик евентов и отрисовщик
    pl.process_events(events, [])
    pl.draw()

    # теперь отрисовываем свои штуки
    draw_solar_system()

    pygame.display.update()
    clock.tick(FPS)
