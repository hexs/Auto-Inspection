from typing import Union, Set, Optional
import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIWindow, UIPanel, UIImage, UIButton, UILabel, UITextEntryLine, UITextBox
from pygame_gui.windows import UIFileDialog
import random
from pygame_gui.core.interfaces import IWindowInterface, IUIManagerInterface


class SetMarkWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect = pygame.Rect(100, 100, 450, 300),
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "Set Mark",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)
        self.is_blocking = True

        self.manager = manager
        self.select_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'select',
                                      self.manager, container=self)
        self.draw_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'draw',
                                    self.manager, container=self)
        self.select_button.disable()
        self.button_focus = 'select'

        self.m1_label = UILabel(pygame.Rect((150, 10 + 30 * 0.5), (60, 30)), 'mark 1:',
                                self.manager, container=self)
        self.m1_label = UILabel(pygame.Rect((150, 10 + 30 * 3), (60, 30)), 'mark 2:',
                                self.manager, container=self)
        self.m1xy_label = UILabel(pygame.Rect((200, 10 + 30 * 0.5), (60, 30)), 'xy:',
                                  self.manager, container=self)
        self.m1wh_label = UILabel(pygame.Rect((200, 10 + 30 * 1.5), (60, 30)), 'wh:',
                                  self.manager, container=self)
        self.m2xy_label = UILabel(pygame.Rect((200, 10 + 30 * 3), (60, 30)), 'xy:',
                                  self.manager, container=self)
        self.m2wh_label = UILabel(pygame.Rect((200, 10 + 30 * 4), (60, 30)), 'wh:',
                                  self.manager, container=self)
        self.m1x = UITextEntryLine(pygame.Rect((260, 10 + 30 * 0.5), (60, 30)), self.manager, self, initial_text='0')
        self.m1y = UITextEntryLine(pygame.Rect((330, 10 + 30 * 0.5), (60, 30)), self.manager, self, initial_text='0')
        self.m1w = UITextEntryLine(pygame.Rect((260, 10 + 30 * 1.5), (60, 30)), self.manager, self, initial_text='0')
        self.m1h = UITextEntryLine(pygame.Rect((330, 10 + 30 * 1.5), (60, 30)), self.manager, self, initial_text='0')

        self.m2x = UITextEntryLine(pygame.Rect((260, 10 + 30 * 3), (60, 30)), self.manager, self, initial_text='0')
        self.m2y = UITextEntryLine(pygame.Rect((330, 10 + 30 * 3), (60, 30)), self.manager, self, initial_text='0')
        self.m2w = UITextEntryLine(pygame.Rect((260, 10 + 30 * 4), (60, 30)), self.manager, self, initial_text='0')
        self.m2h = UITextEntryLine(pygame.Rect((330, 10 + 30 * 4), (60, 30)), self.manager, self, initial_text='0')

        self.ok_button = UIButton(pygame.Rect((200, 10 + 30 * 6), (100, 30)), 'OK',
                                  self.manager, container=self)
        self.cancel_button = UIButton(pygame.Rect((300, 10 + 30 * 6), (100, 30)), 'Cancel',
                                      self.manager, container=self)

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.select_button:
                self.select_button.disable()
                self.draw_button.enable()
                self.button_focus = 'select'

            if event.ui_element == self.draw_button:
                self.draw_button.disable()
                self.select_button.enable()
                self.button_focus = 'draw'

    def update(self, time_delta):
        super().update(time_delta)


class SetFrameWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect = pygame.Rect(100, 100, 600, 300),
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "Set Frame",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)
        self.is_blocking = True

        self.manager = manager
        self.select_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'select',
                                      self.manager, container=self)
        self.draw_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'draw',
                                    self.manager, container=self)
        self.select_button.disable()
        self.button_focus = 'select'

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.select_button:
                self.select_button.disable()
                self.draw_button.enable()
                self.button_focus = 'select'

            if event.ui_element == self.draw_button:
                self.draw_button.disable()
                self.select_button.enable()
                self.button_focus = 'draw'

    def update(self, time_delta):
        super().update(time_delta)


class DebugWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect = pygame.Rect(100, 100, 300, 300),
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "Debug",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)
        self.is_blocking = True

        self.manager = manager
        self.set_mark_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'set mark',
                                        self.manager, container=self)
        self.set_mark_res = UITextBox('X', pygame.Rect((120, 10 + 30 * 1), (40, 30)), self.manager, container=self)
        self.set_frame_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'set frame',
                                         self.manager, container=self)
        self.set_frame_res = UITextBox('X', pygame.Rect((120, 10 + 30 * 2), (40, 30)), self.manager, container=self)
        self.save_button = UIButton(pygame.Rect((10, 10 + 30 * 4), (100, 30)), 'save',
                                    self.manager, container=self)

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(event)
            if event.ui_element == self.set_frame_button:
                set_frame = SetFrameWindow(manager=self.manager)
                self.set_frame_res.set_text('ok')

            if event.ui_element == self.set_mark_button:
                set_mark = SetMarkWindow(manager=self.manager)
                self.set_mark_res.set_text('ok')
                
    def update(self, time_delta):
        super().update(time_delta)


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Image Load App')
    window_surface = pygame.display.set_mode((800, 600))
    ui_manager = pygame_gui.UIManager((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(ui_manager.ui_theme.get_colour('dark_bg'))

    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 50 * 1, 150, 30),
                                               text='debug',
                                               manager=ui_manager)
    set_mark_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 50 * 2, 150, 30),
                                                   text='set_mark',
                                                   manager=ui_manager)
    set_frame_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 50 * 3, 150, 30),
                                                    text='set_frame',
                                                    manager=ui_manager)

    display_loaded_image = None

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            ui_manager.process_events(event)
            # if event.type not in [1024]:
            #     print(event)
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == load_button:
                    debug_window = DebugWindow(manager=ui_manager)
                if event.ui_element == set_mark_button:
                    set_mark_window = SetMarkWindow(manager=ui_manager)
                if event.ui_element == set_frame_button:
                    set_frame_window = SetFrameWindow(manager=ui_manager)

        ui_manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        ui_manager.draw_ui(window_surface)

        pygame.display.update()
