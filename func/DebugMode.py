from typing import Union, Set, Optional
import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog
import random


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


class DebugMode(UIManager):
    def __init__(self, manager: pygame_gui.UIManager, manager_image: pygame_gui.UIManager):
        self.select_button = UIButton(pygame.Rect((1337, 70 + 30 * 0), (100, 30)), 'select', manager)
        self.set_mark_button = UIButton(pygame.Rect((1337, 70 + 30 * 1), (100, 30)), 'set mark', manager)
        self.set_frame_button = UIButton(pygame.Rect((1337, 70 + 30 * 2), (100, 30)), 'set frame', manager)
        self.image_rect = manager_image.get_root_container().get_rect()
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

    def reset_drawing(self):
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

    def process_events(self, event, data, image_mouse_pos):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.select_button:
                data['tool'] = 'select'
            elif event.ui_element == self.set_mark_button:
                data['tool'] = 'set mark'
                self.reset_drawing()
            elif event.ui_element == self.set_frame_button:
                data['tool'] = 'set frame'
                self.reset_drawing()

        if image_mouse_pos and data['mode'] == 'debug' and data['tool'] in ['set frame', 'set mark']:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.end_pos = None
                    self.start_pos = image_mouse_pos
                    self.drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.drawing = False

        if self.end_pos and self.end_pos:
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.dict['key'] == pygame.K_RIGHT:
                    self.start_pos = self.start_pos[0] + 1, self.start_pos[1]
                    self.end_pos = self.end_pos[0] + 1, self.end_pos[1]
                elif event.dict['key'] == pygame.K_LEFT:
                    self.start_pos = self.start_pos[0] - 1, self.start_pos[1]
                    self.end_pos = self.end_pos[0] - 1, self.end_pos[1]
                elif event.dict['key'] == pygame.K_UP:
                    self.start_pos = self.start_pos[0], self.start_pos[1] - 1
                    self.end_pos = self.end_pos[0], self.end_pos[1] - 1
                elif event.dict['key'] == pygame.K_DOWN:
                    self.start_pos = self.start_pos[0], self.start_pos[1] + 1
                    self.end_pos = self.end_pos[0], self.end_pos[1] + 1

                elif event.dict['key'] == pygame.K_KP_PLUS:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        self.end_pos = self.end_pos[0] + 1, self.end_pos[1]
                    else:
                        self.end_pos = self.end_pos[0], self.end_pos[1] + 1
                elif event.dict['key'] == pygame.K_KP_MINUS:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        self.end_pos = self.end_pos[0] - 1, self.end_pos[1]
                    else:
                        self.end_pos = self.end_pos[0], self.end_pos[1] - 1
                elif event.dict['key'] == pygame.K_KP_MULTIPLY:
                    self.end_pos = self.end_pos[0] + 1, self.end_pos[1]
                elif event.dict['key'] == pygame.K_KP_DIVIDE:
                    self.end_pos = self.end_pos[0] - 1, self.end_pos[1]

            elif event.type == pygame.TEXTINPUT:
                if event.dict['text'] == 'd':
                    self.start_pos = self.start_pos[0] + 10, self.start_pos[1]
                    self.end_pos = self.end_pos[0] + 10, self.end_pos[1]
                elif event.dict['text'] == 'a':
                    self.start_pos = self.start_pos[0] - 10, self.start_pos[1]
                    self.end_pos = self.end_pos[0] - 10, self.end_pos[1]
                elif event.dict['text'] == 'w':
                    self.start_pos = self.start_pos[0], self.start_pos[1] - 10
                    self.end_pos = self.end_pos[0], self.end_pos[1] - 10
                elif event.dict['text'] == 's':
                    self.start_pos = self.start_pos[0], self.start_pos[1] + 10
                    self.end_pos = self.end_pos[0], self.end_pos[1] + 10



    def uupdate(self, image_surface, data, image_mouse_pos):
        self.image_mouse_pos = image_mouse_pos
        # ---  เส้นประ  --------------------------------
        if image_mouse_pos and data['mode'] == 'debug':
            if data['tool'] in ['set frame', 'set mark']:
                x, y = image_mouse_pos
                pygame.draw.line(image_surface, (255, 255, 255), (x, 0), (x, 1399), 1)
                pygame.draw.line(image_surface, (255, 255, 255), (0, y), (999, y), 1)
                for i in range(0, 999, 10):
                    pygame.draw.line(image_surface,
                                     (random.randint(0, 200), random.randint(0, 100), random.randint(0, 200)),
                                     (x, i), (x, i + 5), 1)
                for i in range(0, 1399, 10):
                    pygame.draw.line(image_surface,
                                     (random.randint(0, 200), random.randint(0, 100), random.randint(0, 200)),
                                     (i, y), (i + 5, y), 1)
        # --- กรอบเหลือง ----------------------------------
        if self.drawing:
            self.end_pos = image_mouse_pos
        if self.start_pos and self.end_pos:
            rect = pygame.Rect(self.start_pos, (
                self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]))
            pygame.draw.rect(image_surface, (20, 20, 20), re_rect(rect, 1), 3)
            pygame.draw.rect(image_surface, (255, 240, 0), re_rect(rect), 1)
            if data['tool'] in ['set mark']:
                pygame.draw.rect(image_surface, (20, 20, 20), rect_2x(rect, 4), 3)
        return image_surface


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Image Load App')
    window_surface = pygame.display.set_mode((800, 600))
    ui_manager = pygame_gui.UIManager((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(ui_manager.ui_theme.get_colour('dark_bg'))

    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 100, 150, 30),
                                               text='Load Image',
                                               manager=ui_manager)

    display_loaded_image = None

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type not in [1024]:
                print(event)
            if event.type == pygame.QUIT:
                is_running = False

            if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                    event.ui_element == load_button):
                pass
            ui_manager.process_events(event)

        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        pygame.display.update()
