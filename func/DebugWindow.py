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
from func.SelectionFrameList import SelectionFrameList


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
            if event.ui_element == self.draw2_button:
                self.draw1_button.enable()
                self.draw2_button.disable()


class SetFrameWindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect = pygame.Rect(100, 100, 500, 400),
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "Set Frame",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect, manager, window_display_title, element_id, object_id, resizable, visible, draggable)

        self.manager = manager
        # self.select_button = UIButton(pygame.Rect((10, 10 + 30 * 1), (100, 30)), 'select',
        #                               self.manager, container=self)
        # self.draw_button = UIButton(pygame.Rect((10, 10 + 30 * 2), (100, 30)), 'draw',
        #                             self.manager, container=self)
        # self.select_button.disable()
        UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 0, 50, 30), text='name', manager=self.manager, container=self)
        UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 1, 50, 30), text='x', manager=self.manager, container=self)
        UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 2, 50, 30), text='y', manager=self.manager, container=self)
        UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 3, 50, 30), text='w', manager=self.manager, container=self)
        UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 4, 50, 30), text='h', manager=self.manager, container=self)
        self.frame_name_entry_line = UITextEntryLine(pygame.Rect(70, 50, 180, 30), self.manager, self)
        self.frame_x_entry_line = UITextEntryLine(pygame.Rect(70, 50 + 30 * 1, 180, 30), self.manager, self)
        self.frame_y_entry_line = UITextEntryLine(pygame.Rect(70, 50 + 30 * 2, 180, 30), self.manager, self)
        self.frame_w_entry_line = UITextEntryLine(pygame.Rect(70, 50 + 30 * 3, 180, 30), self.manager, self)
        self.frame_h_entry_line = UITextEntryLine(pygame.Rect(70, 50 + 30 * 4, 180, 30), self.manager, self)

        self.frame_list = SelectionFrameList(
            relative_rect=pygame.Rect(260, 50, 200, 200),
            item_list=[('Item 1', (10, 20, 30, 20)),
                       ('Item 2', (10, 20, 30, 20))
                       ],
            manager=self.manager,
            container=self
        )

        self.add_button = UIButton(relative_rect=pygame.Rect(10, 260, 75, 30),
                                   text='Add', manager=self.manager, container=self)
        self.save_button = UIButton(relative_rect=pygame.Rect(85, 260, 75, 30),
                                    text='Save', manager=self.manager, container=self)
        self.delete_button = UIButton(relative_rect=pygame.Rect(210, 260, 75, 30),
                                      text='Delete', manager=self.manager, container=self)

    def process_event(self, event: pygame.event.Event) -> bool:
        super().process_event(event)
        # if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #     if event.ui_element == self.select_button:
        #         self.select_button.disable()
        #         self.draw_button.enable()
        #
        #     if event.ui_element == self.draw_button:
        #         self.draw_button.disable()
        #         self.select_button.enable()

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.add_button:
                name = self.frame_name_entry_line.get_text()
                x = float(self.frame_x_entry_line.get_text())
                y = float(self.frame_y_entry_line.get_text())
                w = float(self.frame_w_entry_line.get_text())
                h = float(self.frame_h_entry_line.get_text())
                if name and x and y and w and h:
                    self.frame_list.add_items([(name, (x, y, w, h)), ])
                    self.frame_name_entry_line.set_text(f'{name[:-1]}{chr(ord(name[-1]) + 1)}')

            elif event.ui_element == self.delete_button:
                selected_list = [item for item in self.frame_list.item_list if item['selected']]
                if len(selected_list):  # ต้อง selected ให้มีข้อมูล
                    selected = selected_list[0]
                    self.frame_list.remove_items([(selected['text'], selected['frame_pos'])])
            # if selected_items:
            #     print(selected_items)
            #     frame_list.remove_items([selected_items])
            # elif event.ui_element == save_button:
            #     selected_items = frame_list.get_single_selection()
            #     entry_box_dict = json.loads(frame_data_entry_box.get_text())
            #     if selected_items is not None:  # ต้อง selected_item
            #         frame_list.remove_item(selected_items)
            #         frame_list.add_item(entry_box_dict['name'], entry_box_dict)



        elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            selected_items = self.frame_list.get_single_selection()
            if selected_items:
                selected_list = [item for item in self.frame_list.item_list if item['selected']]
                if len(selected_list):  # ต้อง selected ให้มีข้อมูล
                    selected = selected_list[0]
                    frame_pos = selected['frame_pos']
                    x, y, w, h = frame_pos
                    self.frame_name_entry_line.set_text(selected['text'])
                    self.frame_x_entry_line.set_text(f'{x}')
                    self.frame_y_entry_line.set_text(f'{y}')
                    self.frame_w_entry_line.set_text(f'{w}')
                    self.frame_h_entry_line.set_text(f'{h}')


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
        self.enable_drawing_if_moues_in_image = True
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

        mouse_pos = pygame.mouse.get_pos()  # ตำแหน่ง mouse
        image_mouse_pos = manager_pos(self.manager_image)  # ตำแหน่ง mouse ในภาพ

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.set_mark_button:
                self.set_mark_window = SetMarkWindow(pygame.Rect(1360, 100, 500, 400), manager=self.manager)
                self.set_mark_res.set_text('ok')
            elif event.ui_element == self.set_frame_button:
                self.set_frame_window = SetFrameWindow(pygame.Rect(1360, 100, 500, 400), manager=self.manager)
                self.set_frame_res.set_text('ok')
                self.set_frame_button.disable()
                self.enable_drawing = True
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.set_frame_window:
                self.enable_drawing = False
                self.set_frame_button.enable()
                self.set_frame_window = None

        elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.set_mark_window:
                self.set_mark_window.button_focus = '-'
            elif event.ui_element == self.set_frame_window:
                self.set_frame_window.button_focus = '-'

        if self.set_frame_window is not None:  # ต้องมี set_frame_window
            if image_mouse_pos and self.enable_drawing:
                if not self.rect.collidepoint(*mouse_pos) and \
                        not self.set_frame_window.rect.collidepoint(*mouse_pos):
                    # mouse_pos จะต้องไม่อยู่ใน self และ self.set_frame_window
                    # จึงจะวาดได้
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    mouse_pos = pygame.mouse.get_pos()
                    if self.set_frame_window.rect.collidepoint(mouse_pos):
                        try:
                            current_text = int(self.set_frame_window.get_text())
                        except ValueError:
                            current_text = 0
                        self.set_frame_window.set_text(str(current_text + 1))
                elif event.button == 5:  # Mouse wheel down
                    mouse_pos = pygame.mouse.get_pos()
                    if self.set_frame_window.rect.collidepoint(mouse_pos):
                        try:
                            current_text = int(self.set_frame_window.get_text())
                        except ValueError:
                            current_text = 0
                        self.set_frame_window.set_text(str(current_text - 1))

    def _update_(self, draw_frame):
        image_mouse_pos = manager_pos(self.manager_image)
        mouse_pos = pygame.mouse.get_pos()
        # กดปุ่มที่กำหนด และ moues_in_img
        draw_frame.enableDrawing(self.enable_drawing and self.enable_drawing_if_moues_in_image)
        if self.set_frame_window is not None:  # ต้องมี set_frame_window
            if not self.rect.collidepoint(*mouse_pos) and \
                    not self.set_frame_window.rect.collidepoint(*mouse_pos):
                self.enable_drawing_if_moues_in_image = True
                if self.drawing:
                    self.end_pos = image_mouse_pos
            else:
                self.enable_drawing_if_moues_in_image = False

            if self.start_pos and self.end_pos:
                draw_frame.add('#crt_drawing', crt=[(255, 255, 0), xyxy2xywh((*self.start_pos, *self.end_pos)), 1])
                # if self.set_mark_window.button_focus in ['m1', 'm2']:
                #     draw_frame.add(f'#{self.set_mark_window.button_focus}',
                #                    crt=[(255, 255, 0), xyxy2xywh((*self.start_pos, *self.end_pos)), 1])

        if self.drawing:
            # ถ้าวาด
            # ให้แสดงข้อความที่ entry_line
            x, y, w, h = draw_frame.rect_list['#crt_drawing'].rect
            print(x, y, w, h)
            self.set_frame_window.frame_x_entry_line.set_text(f'{x}')
            self.set_frame_window.frame_y_entry_line.set_text(f'{y}')
            self.set_frame_window.frame_w_entry_line.set_text(f'{w}')
            self.set_frame_window.frame_h_entry_line.set_text(f'{h}')


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
