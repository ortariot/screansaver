#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
from pygame.constants import K_1

from pygame.version import ver

SCREEN_DIM = (800, 600)


# =======================================================================================
# Vector class
# =======================================================================================

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def vec(self):
        """возвращает пару координат, определяющих вектор
        (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с
        системы координат (0, 0)"""
        return self.x, self.y

    def int_pair(self):
        return (int(self.x), int(self.y))


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_vec2d(self, vec, speed):

        self.points.append(vec)
        self.speeds.append(speed)

    def pluse_speed(self, value_x, value_y):  
        for spd in self.speeds:
            spd.x += value_x
            spd.y += value_y

    def minus_speed(self, value_x, value_y):
        for spd in self.speeds:
            spd.x = 0
            spd.y = 0 


    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)
        

    def draw_points(self, style="points",
                    width=3,
                    color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, 
                                 self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(),
                                 width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(),
                                   width
                                   )

class Knot(Polyline):

    line_points = []
    steps = 35

    def add_vec2d(self, vec: Vec2d, speed: Vec2d):
        vec_x, vec_y = vec
        spd_x, spd_y = speed
        super().add_vec2d(Vec2d(vec_x, vec_y), Vec2d(spd_x, spd_y))
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def set_steps(self, count):
        self.count = count

    def get_steps(self):
        return self.steps


    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return (base_points[deg] * alpha) + (self.get_point(base_points, alpha, deg - 1) * (1 - alpha))


    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        self.line_points = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.line_points.extend(self.get_points(ptn, self.steps))
        return self.line_points

    def draw_points(self, style="points",
                    width=3,
                    color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.line_points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 self.line_points[p_n].int_pair(),
                                 self.line_points[p_n + 1].int_pair(),
                                 width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(),
                                   width
                                   )



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
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    line = Knot()
    line2 = Knot()
    curves = [Knot() for i in range(10)]
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
                    curves = [Knot() for i in range(10)]
                    line = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_0]:
                        steps = curves[0].get_steps() + 1
                        curves[0].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_1]:
                        steps = curves[1].get_steps() + 1
                        curves[1].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_2]:
                        steps = curves[2].get_steps() + 1
                        curves[2].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_3]:
                        steps = curves[3].get_steps() + 1
                        curves[3].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_4]:
                        steps = curves[4].get_steps() + 1
                        curves[4].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_5]:
                        steps = curves[5].get_steps() + 1
                        curves[5].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_6]:
                        steps = curves[6].get_steps() + 1
                        curves[6].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_7]:
                        steps = curves[7].get_steps() + 1
                        curves[7].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_8]:
                        steps = curves[8].get_steps() + 1
                        curves[8].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_PLUS] and pygame.key.get_pressed()[pygame.K_9]:
                        steps = curves[9].get_steps() + 1
                        curves[9].set_steps(steps)         
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_0]:
                        steps = curves[0].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[0].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_1]:
                        steps = curves[1].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[1].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_2]:
                        steps = curves[2].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[2].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_3]:
                        steps = curves[3].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[3].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_4]:
                        steps = curves[4].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[4].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_5]:
                        steps = curves[5].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[5].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_6]:
                        steps = curves[6].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[6].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_7]:
                        steps = curves[7].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[7].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_8]:
                        steps = curves[8].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[8].set_steps(steps)
                    if pygame.key.get_pressed()[pygame.K_KP_MINUS] and pygame.key.get_pressed()[pygame.K_9]:
                        steps = curves[9].get_steps() - 1 if curves[0].get_steps() > 1 else 0
                        curves[9].set_steps(steps)    
                if event.key == pygame.K_MINUS:
                    if pygame.key.get_pressed()[pygame.K_MINUS] and pygame.key.get_pressed()[pygame.K_1]:
                        curves[1].minus_speed(0.2, 0.2)

                if event.key == pygame.K_EQUALS:
                    print('pkuse')
                    if pygame.key.get_pressed()[pygame.K_EQUALS] and pygame.key.get_pressed()[pygame.K_1]:
                        curves[1].pluse_speed(0.2, 0.2)




        
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_0]:
                    curves[0].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_1]:
                    curves[1].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_2]:
                    curves[2].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_3]:
                    curves[3].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_4]:
                    curves[4].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_5]:
                    curves[5].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_6]:
                    curves[6].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_7]:
                    curves[7].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_8]:
                    curves[8].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))
                if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_9]:
                    curves[9].add_vec2d(event.pos, (random.random() * 2, random.random() * 2))    
                


        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        for curve in curves:
            curve.draw_points()
            curve.draw_points('line', 3, color)

        if not pause:
            for curve in curves:
                curve.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)