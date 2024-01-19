from typing import Union, Set, Optional
import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog


class DebugMode(UIManager):
    def __init__(self, rect: pygame.Rect, manager: pygame_gui.UIManager):
        self.select_button = UIButton(pygame.Rect((1337, 70 + 30 * 0), (100, 30)), 'select', manager)
        self.set_mark_button = UIButton(pygame.Rect((1337, 70 + 30 * 1), (100, 30)), 'set mark', manager)
        self.set_frame_button = UIButton(pygame.Rect((1337, 70 + 30 * 2), (100, 30)), 'set frame', manager)

    def process_events(self, event):
        if event.ui_element == self.select_button:
            data['tool'] = 'select'

        elif event.ui_element == self.set_mark_button:
            data['tool'] = 'set mark'
            start_pos = None
            end_pos = None
            drawing = False

        elif event.ui_element == self.set_frame_button:
            data['tool'] = 'set frame'
            start_pos = None
            end_pos = None
            drawing = False


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
