from typing import Union, Set, Optional
import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIWindow, UIPanel, UIImage, UIButton, UILabel, UITextEntryLine, UITextBox
from pygame_gui.windows import UIFileDialog
import random
from pygame_gui.core.interfaces import IWindowInterface, IUIManagerInterface
from func.about_point import xyxy2xywh


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

        self.manager = manager
        self.draw1_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'mark 1',
                                     self.manager, container=self)
        self.draw2_button = UIButton(pygame.Rect((10, 10 + 30 * 3), (100, 30)), 'mark 2',
                                     self.manager, container=self)
        self.button_focus = '-'

        self.m1_label = UILabel(pygame.Rect((150, 10 + 30 * 0.5), (60, 30)), 'mark 1:',
                                self.manager, container=self)
        self.m2_label = UILabel(pygame.Rect((150, 10 + 30 * 3), (60, 30)), 'mark 2:',
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

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.draw1_button:
                self.draw1_button.disable()
                self.draw2_button.enable()
                self.button_focus = 'm1'
            if event.ui_element == self.draw2_button:
                self.draw1_button.enable()
                self.draw2_button.disable()
                self.button_focus = 'm2'


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

        self.manager = manager
        self.select_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'select',
                                      self.manager, container=self)
        self.draw_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'draw',
                                    self.manager, container=self)
        self.select_button.disable()

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.select_button:
                self.select_button.disable()
                self.draw_button.enable()

            if event.ui_element == self.draw_button:
                self.draw_button.disable()
                self.select_button.enable()


class DebugWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect = pygame.Rect(100, 100, 300, 300),
                 manager: Optional[IUIManagerInterface] = None,
                 manager_image: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "Debug",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)

        self.set_mark_window = None
        self.set_frame_window = None
        self.enable_drawing = False
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

        self.manager = manager
        self.manager_image = manager_image
        self.set_mark_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'set mark',
                                        self.manager, container=self)
        self.set_mark_res = UITextBox('X', pygame.Rect((120, 10 + 30 * 1), (40, 30)), self.manager, container=self)
        self.set_frame_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'set frame',
                                         self.manager, container=self)
        self.set_frame_res = UITextBox('X', pygame.Rect((120, 10 + 30 * 2), (40, 30)), self.manager, container=self)
        self.save_button = UIButton(pygame.Rect((10, 10 + 30 * 4), (100, 30)), 'save',
                                    self.manager, container=self)

    def reset_drawing(self):
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)

        mouse_pos = pygame.mouse.get_pos()
        image_mouse_pos = manager_pos(self.manager_image)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.set_mark_button:
                self.set_mark_window = SetMarkWindow(manager=self.manager)
                self.set_mark_res.set_text('ok')
            elif event.ui_element == self.set_frame_button:
                self.set_frame_window = SetFrameWindow(manager=self.manager)
                self.set_frame_res.set_text('ok')

        elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.set_mark_window:
                self.set_mark_window.button_focus = '-'
            elif event.ui_element == self.set_frame_window:
                self.set_frame_window.button_focus = '-'

        if image_mouse_pos and self.enable_drawing:
            if not self.rect.collidepoint(*mouse_pos) and \
                    not self.set_mark_window.rect.collidepoint(*mouse_pos):
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

    def _update_(self, draw_frame):
        image_mouse_pos = manager_pos(self.manager_image)
        mouse_pos = pygame.mouse.get_pos()
        draw_frame.enable_drawing = self.enable_drawing

        if self.set_mark_window and \
                not self.rect.collidepoint(*mouse_pos) and \
                not self.set_mark_window.rect.collidepoint(*mouse_pos):
            if self.drawing:
                self.end_pos = image_mouse_pos

            if self.set_mark_window.button_focus in ['m1', 'm2']:
                self.enable_drawing = True
            else:
                self.enable_drawing = False

            if self.start_pos and self.end_pos:
                draw_frame.add('#crt_drawing', crt=[(255, 255, 0), xyxy2xywh((*self.start_pos, *self.end_pos)), 1])
                if self.set_mark_window.button_focus in ['m1', 'm2']:
                    draw_frame.add(f'#{self.set_mark_window.button_focus}',
                                   crt=[(255, 255, 0), xyxy2xywh((*self.start_pos, *self.end_pos)), 1])


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
