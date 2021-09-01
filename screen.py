#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return self.x - other.x, self.y - other.y

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return self.x + other.x, self.y + other.y

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return self.x * k, self.y * k

    def vec(self):
        """возвращает пару координат, определяющих вектор
        (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с
        системы координат (0, 0)"""
        return self.x, self.y

    def int_pair(self):
        return (self.x, self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_vec2d(self, vec: Vec2d, speed: Vec2d):
        self.points.append(vec)
        self.speeds.append(speed)

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, style="points",
                    width=3,
                    color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points[p_n].x),
                                  int(self.points[p_n].y)
                                  ),
                                 (int(self.points[p_n + 1].x),
                                  int(self.points[p_n + 1].y)
                                  ),
                                 width
                                 )

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)),
                                   width
                                   )


class Knot(Polyline):

    def add_vec2d(self, vec: Vec2d, speed: Vec2d):
        super().add_vec2d(vec, speed)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def set_steps(self, count):
        self.count = count

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.points) - 1
        if deg == 0:
            return self.points[0]
        return self.points[deg] * alpha, self.get_point(alpha, deg - 1) * (1 - alpha)
        # return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(self.points[i] + self.points[i + 1])
            print(ptn[0].x)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]))

            res.extend(self.get_points(ptn, self.count))
        return res



# =======================================================================================
# Функции отрисовки
# =======================================================================================
# def draw_points(points, style="points", width=3, color=(255, 255, 255)):
#     """функция отрисовки точек на экране"""
#     if style == "line":
#         for p_n in range(-1, len(points) - 1):
#             pygame.draw.line(gameDisplay, color,
#                              (int(points[p_n][0]), int(points[p_n][1])),
#                              (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

#     elif style == "points":
#         for p in points:
#             pygame.draw.circle(gameDisplay, color,
#                                (int(p[0]), int(p[1])), width)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
# def get_point(points, alpha, deg=None):
#     if deg is None:
#         deg = len(points) - 1
#     if deg == 0:
#         return points[0]
#     return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))


# def get_points(base_points, count):
#     alpha = 1 / count
#     res = []
#     for i in range(count):
#         res.append(get_point(base_points, i * alpha))
#     return res


# def get_knot(points, count):
#     if len(points) < 3:
#         return []
#     res = []
#     for i in range(-2, len(points) - 2):
#         ptn = []
#         ptn.append(mul(add(points[i], points[i + 1]), 0.5))
#         ptn.append(points[i + 1])
#         ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

#         res.extend(get_points(ptn, count))
#     return res


# def set_points(points, speeds):
#     """функция перерасчета координат опорных точек"""
#     for p in range(len(points)):
#         points[p] = add(points[p], speeds[p])
#         if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
#             speeds[p] = (- speeds[p][0], speeds[p][1])
#         if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
#             speeds[p] = (speeds[p][0], -speeds[p][1])


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    # points = []
    # speeds = []
    line = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line = Knot()
                    # points = []
                    # speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                line.set_steps(steps)
                line.add_vec2d( Vec2d(event.pos[0], event.pos[1]) , Vec2d(random.random() * 2, random.random() * 2))
                # points.append(event.pos)
                # speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        line.draw_points()
        line.draw_points('line')
        # draw_points(points)
        # draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            line.set_points()
            # set_points(points, speeds)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)