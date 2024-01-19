from typing import Union, Set, Optional
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.windows import UIFileDialog


class LoadFileWindow(UIFileDialog):
    def __init__(self,
                 rect: pygame.Rect,
                 manager: pygame_gui.UIManager,
                 window_title: str = 'Load...',
                 allowed_suffixes: Set[str] = {""},
                 initial_file_path: Optional[str] = None,
                 object_id: Union[ObjectID, str] = ObjectID('#file_dialog', None),
                 ):
        super().__init__(rect, manager, window_title, allowed_suffixes, initial_file_path, object_id)


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
                file_dialog = LoadFileWindow(pygame.Rect(160, 50, 440, 500),
                                         ui_manager,
                                         allowed_suffixes={".png"},
                                         # object_id=ObjectID('#load_image', None),
                                         )
            ui_manager.process_events(event)

        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        pygame.display.update()
