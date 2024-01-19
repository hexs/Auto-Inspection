import os
import sys
from datetime import datetime
from pprint import pprint
import cv2
import numpy as np
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel, UITextBox, UIButton, UIHorizontalSlider
from pygame_gui.elements import UIWindow, UIPanel, UIImage
from pygame_gui.windows import UIFileDialog

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

def is_mouse_in_manager(manager):
    manager_rect = manager.get_root_container().get_rect()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return manager_rect.collidepoint(mouse_x, mouse_y)


def manager_pos(manager, float=False):
    manager_rect = manager.get_root_container().get_rect()
    x, y, w, h = manager_rect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if manager_rect.collidepoint(mouse_x, mouse_y):
        return mouse_x - manager_rect.x, mouse_y - manager_rect.y
    else:
        return None


def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    if type(None) == type(image):
        image = np.full((1000, 1000 * 4 // 3, 3), (222, 222, 222), np.uint8)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (1000 * 4 // 3, 1000))
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")



def main(data):
    import random

    pygame.init()
    pygame.display.set_caption('Auto Inspection')
    display = pygame.display.set_mode((1920, 1080))
    background = pygame.Surface((1920, 1080))
    background.fill((188, 205, 217))
    pygame.draw.rect(background, (255, 255, 255), pygame.Rect(1, 31, 1920 - 2, 25))
    pygame.draw.rect(background, (255, 255, 255), pygame.Rect(1434 - 98, 58, 585 - 2, 1000))

    title_bar = pygame.Surface((1920, 30))
    title_bar.fill((204, 221, 236))
    status_bar = pygame.Surface((1920, 20))
    status_bar.fill((204, 221, 236))

    # UI
    manager = pygame_gui.UIManager((1920, 1080), 'UI/themes/manager_main.json')
    manager_image = pygame_gui.UIManager((1000 * 4 // 3, 1000), 'UI/themes/manager_main.json')
    manager_image.get_root_container().get_rect().topleft = 1, 58
    image_form_cam = data['capture'][1]
    image_surface = cvimage_to_pygame(data['capture'][1])
    log_window = UIWindow(rect=pygame.Rect((600, 777), (1300 + 33, 270 + 60)),
                          manager=manager, resizable=True,
                          window_display_title='Log window')

    minimize = UIButton(pygame.Rect((1920 - 45 * 3, 0), (45, 30)), '', manager,
                        object_id=ObjectID(class_id='@minimize', object_id='#Button'))
    maximize = UIButton(pygame.Rect((1920 - 45 * 2, 0), (45, 30)), '', manager,
                        object_id=ObjectID(class_id='@maximize', object_id='#Button'))
    close = UIButton(pygame.Rect((1920 - 45 * 1, 0), (45, 30)), '', manager,
                     object_id=ObjectID(class_id='@close', object_id='#Button'))
    debug_button = UIButton(pygame.Rect((160 + 60 * 0, 30), (60, 28)), 'debug', manager)
    manual_button = UIButton(pygame.Rect((160 + 60 * 1, 30), (60, 28)), 'manual', manager)
    auto_button = UIButton(pygame.Rect((160 + 60 * 2, 30), (60, 28)), 'auto', manager)
    capture_button = UIButton(pygame.Rect((160 + 60 * 4, 30), (60, 28)), 'capture', manager)
    load_button = UIButton(pygame.Rect((160 + 60 * 5, 30), (60, 28)), 'Load Image', manager)

    select_button = UIButton(pygame.Rect((1337, 70 + 30 * 0), (100, 30)), 'select', manager)
    set_frame_button = UIButton(pygame.Rect((1337, 70 + 30 * 1), (100, 30)), 'set frame', manager)

    fps_label = UILabel(pygame.Rect(10, 1060, 50, 20), "-", manager)
    mouse_pos_label = UILabel(pygame.Rect(80, 1060, 200, 20), "-", manager, )
    image_pos_label = UILabel(pygame.Rect(270, 1060, 500, 20), "-", manager, )
    status_cam = UILabel(pygame.Rect(500, 1060, 500, 20), "-", manager, )
    log_label = UILabel(pygame.Rect(670, 1060, 500, 20), "-", manager, )

    htm_text = UITextBox('', pygame.Rect((0, 0), (1300, 270)), manager=manager, container=log_window)
    t = []
    # htm_text.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)



    start_pos = None
    end_pos = None
    drawing = False
    clock = pygame.time.Clock()
    while data['is_running']:
        time_delta = clock.tick(60) / 1000.0
        image_mouse_pos = manager_pos(manager_image)
        main_mouse_pos = pygame.mouse.get_pos()
        image_surface = cvimage_to_pygame(image_form_cam)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                data['is_running'] = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == minimize:
                    pygame.display.iconify()
                elif event.ui_element == maximize:
                    data['stop capture'] = True
                elif event.ui_element == close:
                    data['is_running'] = False

                elif event.ui_element == capture_button:
                    image_form_cam = data['capture'][1]

                elif event.ui_element == debug_button:
                    data['mode'] = 'debug'
                elif event.ui_element == manual_button:
                    data['mode'] = 'manual'
                elif event.ui_element == auto_button:
                    data['mode'] = 'auto'
                elif event.ui_element == load_button:
                    load_button.disable()
                    file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                               manager,
                                               window_title='Load Image...',
                                               initial_file_path='data/images/',
                                               allow_picking_directories=True,
                                               allow_existing_files_only=True,
                                               allowed_suffixes={""})


                # debug mode
                elif event.ui_element == select_button:
                    data['tool'] = 'select'
                elif event.ui_element == set_frame_button:
                    data['tool'] = 'set frame'
                    start_pos = None
                    end_pos = None
                    drawing = False

            if (event.type == pygame_gui.UI_WINDOW_CLOSE
                    and event.ui_element == file_dialog):
                load_button.enable()
                file_dialog = None

            if image_mouse_pos and data['mode'] == 'debug' and data['tool'] == 'set frame':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        end_pos = None
                        start_pos = image_mouse_pos
                        drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        drawing = False

        # ---  เส้นประ  --------------------------------
        if image_mouse_pos and data['mode'] == 'debug' and data['tool'] == 'set frame':
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
        if drawing:
            end_pos = image_mouse_pos
        if start_pos and end_pos:
            rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
            pygame.draw.rect(image_surface, (20, 20, 20), re_rect(rect, 1), 3)
            pygame.draw.rect(image_surface, (255, 240, 0), re_rect(rect), 1)

        fps_label.set_text(f'{clock.get_fps():.0f}fps')
        mouse_pos_label.set_text(f'mouse pos:{pygame.mouse.get_pos()}')
        image_pos_label.set_text(f"Image mouse pos:{manager_pos(manager_image)}")
        status_cam.set_text(f"status cam:{data['capture'][0]}")
        log_label.set_text(f"{data['mode']} {data['tool']} {start_pos, end_pos}")

        display.blit(background, (0, 0))
        display.blit(title_bar, (0, 0))

        display.blit(status_bar, (0, 1080 - 20))

        display.blit(image_surface, manager_image.get_root_container().get_rect().topleft)

        manager.update(time_delta)
        manager.draw_ui(display)

        pygame.display.update()


if __name__ == '__main__':
    data = {}
    data['capture'] = (False, None)
    data['stop capture'] = False
    data['reconnect_cam'] = False
    data['is_running'] = True
    data['mode'] = 'debug'  # debug, manual, auto
    data['tool'] = 'select'  # select,set frame
    main(data)












