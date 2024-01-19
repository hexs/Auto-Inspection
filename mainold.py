import os
import statistics
import time
from datetime import datetime
import pygame_gui
import cv2
import numpy as np
import pygame
import sys
from func.Button import Button


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    if type(None) == type(image):
        image = np.full((1008, 1344, 3), (30, 50, 25), np.uint8)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")


class Text:
    def __init__(self, text, pos, font):
        self.text = text
        self.pos = pos
        self.font = font
        self.font_name = 'ui/NotoSansThai.ttf'
        self.font_size = font


    def putText(self, display):



class Texts:
    def __init__(self, font):
        self.texts = {}
        self.font_name = 'ui/NotoSansThai.ttf'
        self.font_size = font


    def add(self, name, pos, text):
        self.texts[name] = Text(text, pos, self.font)

    def putTextall(self, display):
        # self.surface = pygame.draw.rect(display, (40, 40, 40), (41, 41, 1385 - 41, 1008))  # center bar
        # self.surface = pygame.Surface((1344, 1008))  # center bar
        for name, text in self.texts.items():
            self.font = pygame.font.Font(self.font_name, self.font_size)
            text_render = text.font.render(text.text, True, (255, 255, 255))
            # pygame.draw.rect(text_render, (67, 69, 74), text_render.get_rect(), 1)
            display.blit(text_render, text.pos)


class Flex:
    def __init__(self, name, xywh, color):
        self.name = name
        self.where_is_mose = None
        self.xywh = xywh
        self.update_rect()
        self.show_flex = True
        self.color = pygame.Color(color)
        self.buttons = {}
        self.texts = {}
        self.texts = Texts(x)
        self.dict_data = {}

    def update_rect(self, xywh=None):
        if xywh is not None:
            self.xywh = xywh
        self.rect = pygame.Rect(*self.xywh)
        self.surface = pygame.Surface((self.rect.w, self.rect.h))

    def add_text(self, text):
        self.buttons[text.name] = text
    def add_button(self, button):
        self.buttons[button.name] = button

    def mouse_on_surface(self, pos):
        return self.rect.collidepoint(pos)

    def have_mouse_on_is(self, mouse_pos):
        res = None
        if self.show_flex:
            for name, button in self.buttons.items():
                if button.is_mouse_over(self.rect, mouse_pos):
                    res = name
        return res

    def draw(self, display, img=None):
        if self.show_flex:
            if img is not None:
                np = cv2.resize(img, (self.rect.w, self.rect.h))
                self.surface = cvimage_to_pygame(np)
            else:
                self.surface.fill(self.color)
            # pygame.draw.rect(self.surface, (67, 69, 74), self.rect.move(-self.rect.x, -self.rect.y), 1)

            # button
            for name, button in self.buttons.items():
                button.draw(self.surface)
            # for name, button in self.buttons.items():
            #     self.surface.blit(button.image,button.rect)
            display.blit(self.surface, (self.rect.x, self.rect.y))

            # text
            self.texts.putTextall(display)


def main(img):
    pygame.init()
    display = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Auto Inspection')
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((1920, 1080), 'themes/quick_theme.json')
    slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(0 - 3, 1025, 1919 + 3 + 3, 25),
                                                    start_value=137,
                                                    value_range=(0, 200),
                                                    manager=manager)

    top_flex = Flex('top_surface', (0, 0, 1920, 40), (55, 71, 103))
    top_flex.add_button(Button('minimize button', (1920 - 47 * 3, 0, 47, 40), "ui/main button/minimize.png", ))
    top_flex.add_button(Button('maximize button', (1920 - 47 * 2, 0, 47, 40), "ui/main button/maximize.png", ))
    top_flex.add_button(Button('close button', (1920 - 47 * 1, 0, 47, 40), "ui/main button/close.png", ))
    top_flex.add_button(Button('setting button', (1920 - 47 * 4, 5, 30, 30), "ui/main button/setting.png", ))


    bottom_flex = Flex('but_surface', (0, 1050, 1920, 30), (43, 45, 48))

    main1_flex = Flex('main1_surface', (0, 41, 200, 984), (255, 255, 10))
    main2_flex = Flex('main2_surface', (500, 41, 200, 984), (255, 10, 10))

    select_model_win = Flex('select model win', (40, 40, 220, 500), (43, 45, 48))
    select_model_win.show_flex = False

    setting_win = Flex('setting win', (1000, 150, 220, 500), (43, 45, 48))
    setting_win.show_flex = False

    time_list = []
    while True:
        time_delta = clock.tick(60) / 1000.0
        t1 = datetime.now()
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        where_is_mose = (
                top_flex.have_mouse_on_is(mouse_pos) or
                bottom_flex.have_mouse_on_is(mouse_pos) or
                select_model_win.have_mouse_on_is(mouse_pos) or
                setting_win.have_mouse_on_is(mouse_pos)
        )

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if event.button == 3:
                select_model_win.show_flex = False
                setting_win.show_flex = False

                if where_is_mose:
                    print(f"Click --> {where_is_mose} <--")
                    if where_is_mose == 'close button':
                        pygame.quit()
                        sys.exit()
                    if where_is_mose == 'minimize button':
                        pygame.display.iconify()
                    if where_is_mose == 'maximize button':
                        top_flex.show_flex = False

                    if where_is_mose == 'select model button':
                        select_model_win.show_flex = True
                        data = os.listdir('data')
                        i = 0
                        for d in data:
                            i += 1
                            select_model_win.add_button(Button(f'{d}', (10, 10 + i * 35, 195, 30),
                                                               "ui/main button/button box.png",
                                                               text=f'          {d}', text_size=14, text_center='l'))

                    if where_is_mose == 'setting button':
                        setting_win.show_flex = True
                        setting_win.add_button(Button('model 1', (10, 10, 195, 30),
                                                      "ui/main button/button box.png",
                                                      text='          model 1', text_size=14, text_center='l'))
                        setting_win.add_button(Button('model 2', (10, 40, 195, 30),
                                                      "ui/main button/button box.png",
                                                      text='          model 2', text_size=14, text_center='l'))
                        setting_win.add_button(Button('model 3', (10, 70, 195, 30),
                                                      "ui/main button/button box.png",
                                                      text='          model 3', text_size=14, text_center='l'))
            manager.process_events(event)

        t2 = datetime.now()
        t_sec = (t2 - t1).total_seconds()
        time_list.append(t_sec)
        if len(time_list) > 20:
            time_list = time_list[1:]

        top_flex.texts.add('AC Switch', (10, 10), f'AC Switch')
        bottom_flex.texts.add('fps', (10, 1055), f'fps: {round(1 / max(0.0001, statistics.mean(time_list)))}')
        bottom_flex.texts.add('pos', (100, 1055), f'pos: {mouse_pos}')
        bottom_flex.texts.add('pos', (300, 1055), f'{slider.value_range}{slider.current_value}')
        bottom_flex.texts.add('name', (1800, 1055), f'Auto Inspection')

        display.fill((21, 20, 24), (0, 0, 1920, 1080))

        top_flex.draw(display)
        bottom_flex.draw(display)
        select_model_win.draw(display)
        setting_win.draw(display)
        slider_value = max(63, min(137, slider.current_value))
        main1_flex.update_rect((0, 41, 1919 * slider_value // 200 - 2, (1919 * slider_value // 200 - 2) * 3 // 4))
        main2_flex.update_rect(
            (1919 * slider_value // 200 + 1, 41, 1919, (1919 - (1919 * slider_value // 200 + 1)) * 3 // 4))
        img = cv2.imread('ui/ac.png')
        main1_flex.draw(display, img)
        main2_flex.draw(display)

        manager.update(time_delta)
        manager.draw_ui(display)

        pygame.display.flip()


main(0)
