import random
import pygame_gui
import pygame
from func.print_color import *
from pprint import pprint


def re_rect(rect, offset=0):
    x, y, w, h = rect
    if w < 0:
        w = -w
        x = x - w
    if h < 0:
        h = -h
        y = y - h
    x = x - offset
    y = y - offset
    w = w + offset * 2
    h = h + offset * 2
    return x, y, w, h


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


class DrawFrame:
    def __init__(self, surface, manager=None):
        self.surface = surface
        self.manager = manager
        self.rect_list = {
            '#crt_drawing': {'crt': [(255, 255, 0), (200, 100, 100, 100), 1]},
            '#m1': {'crt': [(255, 255, 255), (300, 100, 20, 30), 1]},
            '#m2': {'crt': [(255, 255, 255), (20, 30, 20, 30), 1]},

        }
        # self.add('a3', crt=[(255, 0, 255), (200, 200, 100, 100), 1])
        # self.add('a3', r=(300, 200, 100, 100),outer_rect=4)
        self.focus_frame = None
        self.enable_drawing = False

    def add(self, name, **kwargs):
        self.rect_list[name] = kwargs
        if kwargs.get('r'):
            r = kwargs.get('r')
            c = kwargs.get('c') if kwargs.get('c') else (255, 255, 255)
            t = kwargs.get('t') if kwargs.get('t') else 1
            self.rect_list[name]['crt'] = [c, r, t]

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
            c, r, t = v['crt']
            outer_rect = v.get('outer_rect')

            # frame
            pygame.draw.rect(surface, (0, 0, 0), re_rect(r, 1), t + 2)
            pygame.draw.rect(surface, c, r, t)
            if outer_rect:
                pygame.draw.rect(surface, (20, 20, 20), rect_2x(r, outer_rect), 3)

            # text
            font = pygame.font.Font('freesansbold.ttf', 10)
            text = font.render(f'{k}', True, (0, 0, 0), (255, 255, 255))
            surface.blit(text, (r[0],r[1]-12))

        pygame.draw.rect(surface, *self.rect_list['#crt_drawing']['crt'])




        # print(WARNING)
        # pprint(self.rect_list)
        # print(ENDC)
        return surface


if __name__ == '__main__':
    import pygame
    import sys

    pygame.init()

    width, height = 800, 600
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Rectangle Example")

    surface = pygame.Surface((700, 500))
    draw_frame = DrawFrame(surface)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_frame.update(surface, (10, 10))

        display.blit(surface, (50, 50))
        pygame.display.flip()

    pygame.quit()
