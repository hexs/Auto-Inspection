import random

import pygame

from func.print_color import *


def re_rect(rect):
    x, y, w, h = rect
    if w < 0:
        w = -w
        x = x - w
    if h < 0:
        h = -h
        y = y - h
    return x, y, w, h


def inCreaseSize(rect: pygame.Rect, increase_amount: int) -> pygame.Rect:
    if isinstance(rect, tuple):
        rect = pygame.Rect(*rect)
    return pygame.Rect(rect.x - increase_amount,
                       rect.y - increase_amount,
                       rect.width + 2 * increase_amount,
                       rect.height + 2 * increase_amount)


def rect_2x(rect, times=2):
    x, y, w, h = rect
    if w < 0:
        w = -w
        x = x - w
    if h < 0:
        h = -h
        y = y - h
    offset_w = w * times
    offset_h = h * times
    x = x - offset_w
    y = y - offset_h
    w = w + offset_w * 2
    h = h + offset_h * 2
    return x, y, w, h


def manager_pos(manager, float=False):
    manager_rect = manager.get_root_container().get_rect()
    x, y, w, h = manager_rect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if manager_rect.collidepoint(mouse_x, mouse_y):
        return mouse_x - manager_rect.x, mouse_y - manager_rect.y
    else:
        return None


class CRT:
    def __init__(self, color: tuple, rect: pygame.Rect, thick: int):
        if isinstance(rect,tuple):
            rect = pygame.Rect(rect)
        self.color = color
        self.rect = rect
        self.thick = thick
        self.index = 0
        self.outer_rect = 0

    def set_outer_rect(self, v: int):
        self.outer_rect = v

    def __str__(self):
        return f'{GREEN}{self.color}{BLUE} {self.rect}{ENDC} {self.thick}'

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == 1:
            return self.color
        elif self.index == 2:
            return self.rect
        elif self.index == 3:
            return self.thick
        else:
            self.index = 0
            raise StopIteration


class DrawFrame:
    def __init__(self, surface, manager=None):
        self.surface = surface
        self.manager = manager
        self.rect_list = {
            # '#crt_drawing': CRT((255, 255, 0), pygame.Rect(200, 100, 100, 100), 1),
            '#m1': CRT((255, 255, 255), pygame.Rect(300, 100, 20, 30), 1),
            '#m2': CRT((255, 255, 255), pygame.Rect(20, 30, 20, 30), 1),

        }
        self.focus_frame = None
        self.enable_drawing = False

    def enableDrawing(self, val=True):
        self.enable_drawing = val

    def add(self, name, crt):
        if isinstance(crt, CRT):
            self.rect_list[name] = crt
        elif isinstance(crt, list) or isinstance(crt, tuple):
            self.rect_list[name] = CRT(*crt)

    def update(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect = pygame.rect.Rect(1, 58, 1333, 1000)
        if rect.collidepoint(mouse_x, mouse_y):
            image_mouse_pos = mouse_x - rect.x, mouse_y - rect.y
        else:
            image_mouse_pos = None

        # surface.fill((100,) * 3)
        if self.enable_drawing:
            # ---  เส้นประ  --------------------------------
            if image_mouse_pos:
                x, y = image_mouse_pos
                pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, 1399), 3)
                pygame.draw.line(surface, (255, 255, 255), (0, y), (999, y), 3)
                for i in range(0, 999, 10):
                    pygame.draw.line(surface,
                                     (random.randint(0, 200), random.randint(0, 100), random.randint(0, 200)),
                                     (x, i), (x, i + 5), 3)
                for i in range(0, 1399, 10):
                    pygame.draw.line(surface,
                                     (random.randint(0, 200), random.randint(0, 100), random.randint(0, 200)),
                                     (i, y), (i + 5, y), 3)

        for k, v in self.rect_list.items():
            if k == '#crt_drawing':
                continue
            # frame
            pygame.draw.rect(surface, (0, 0, 0), inCreaseSize(v.rect, 1), v.thick + 2)
            pygame.draw.rect(surface, *v)
            if v.outer_rect:
                pygame.draw.rect(surface, (20, 20, 20), rect_2x(v.rect, v.outer_rect), 3)

            # text
            font = pygame.font.Font('freesansbold.ttf', 10)
            text = font.render(f'{k}', True, (0, 0, 0), (255, 255, 255))
            surface.blit(text, v.rect.move(0, 12))

        # frame
        if self.rect_list.get('#crt_drawing'):
            v = self.rect_list['#crt_drawing']
            pygame.draw.rect(surface, (0, 0, 0), inCreaseSize(v.rect, 1), v.thick + 2)
            pygame.draw.rect(surface, *v)

        return surface
