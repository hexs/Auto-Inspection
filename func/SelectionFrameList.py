import json
from typing import Union, List, Tuple, Optional, Dict
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface, UIElement, ObjectID, UIContainer
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UISelectionList, UIButton, UIPanel, UITextEntryBox, UIVerticalScrollBar, \
    UITextEntryLine, UILabel
import pygame
import pygame_gui


class SelectionFrameList(UISelectionList):
    def __init__(self,
                 relative_rect: pygame.Rect,
                 item_list: Union[List[str], List[Tuple[str, str]], List[Tuple[str, Tuple]]],
                 manager: Optional[IUIManagerInterface] = None,
                 *,
                 allow_multi_select: bool = False,
                 allow_double_clicks: bool = True,
                 container: Optional[IContainerLikeInterface] = None,
                 starting_height: int = 1,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,
                 default_selection: Optional[Union[
                     str, Tuple[str, str],  # Single-selection lists
                     List[str], List[Tuple[str, str]]  # Multi-selection lists
                 ]] = None,
                 ):
        super().__init__(relative_rect,
                         item_list,
                         manager,
                         allow_multi_select=allow_multi_select,
                         allow_double_clicks=allow_double_clicks,
                         container=container,
                         starting_height=starting_height,
                         parent_element=parent_element,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible,
                         default_selection=default_selection)

    def add_items(self, new_items: Union[List[str], List[Tuple[str, str]], List[Tuple[str, Tuple]]]) -> None:
        """
        Add any number of new items to the selection list. Uses the same format
        as when the list is first created.

        :param new_items: the list of new items to add
        """
        super().add_items(new_items)

    def set_item_list(self, new_item_list: Union[List[str], List[Tuple[str, str]]]):
        """
        Set a new string list (or tuple of strings & ids list) as the item list for this selection
        list. This will change what is displayed in the list.

        Tuples should be arranged like so:

         (list_text, object_ID)

         - list_text: displayed in the UI
         - object_ID: used for theming and events

        :param new_item_list: The new list to switch to. Can be a list of strings or tuples.

        """
        self._raw_item_list = new_item_list
        self.item_list = []  # type: List[Dict]
        index = 0
        for new_item in new_item_list:
            if isinstance(new_item, tuple) or isinstance(new_item, list):
                x, y, h, w, = new_item[1]
                new_item_list_item = {'text': new_item[0],
                                      'button_element': None,
                                      'selected': False,
                                      'object_id': '#item_list_item',
                                      'height': index * self.list_item_height,
                                      'frame_pos': (x, y, h, w)
                                      }

            else:
                raise ValueError('Invalid, item must be (tuple,) or [list,]')

            self.item_list.append(new_item_list_item)
            index += 1

        self.total_height_of_list = self.list_item_height * len(self.item_list)
        self.lowest_list_pos = (self.total_height_of_list -
                                self.list_and_scroll_bar_container.relative_rect.height)
        inner_visible_area_height = self.list_and_scroll_bar_container.relative_rect.height

        if self.total_height_of_list > inner_visible_area_height:
            # we need a scroll bar
            self.current_scroll_bar_width = self.scroll_bar_width
            percentage_visible = inner_visible_area_height / max(self.total_height_of_list, 1)

            if self.scroll_bar is not None:
                self.scroll_bar.reset_scroll_position()
                self.scroll_bar.set_visible_percentage(percentage_visible)
                self.scroll_bar.start_percentage = 0
            else:
                self.scroll_bar = UIVerticalScrollBar(pygame.Rect(-self.scroll_bar_width,
                                                                  0,
                                                                  self.scroll_bar_width,
                                                                  inner_visible_area_height),
                                                      visible_percentage=percentage_visible,
                                                      manager=self.ui_manager,
                                                      parent_element=self,
                                                      container=self.list_and_scroll_bar_container,
                                                      anchors={'left': 'right',
                                                               'right': 'right',
                                                               'top': 'top',
                                                               'bottom': 'bottom'})
                self.join_focus_sets(self.scroll_bar)
        else:
            if self.scroll_bar is not None:
                self.scroll_bar.kill()
                self.scroll_bar = None
            self.current_scroll_bar_width = 0

        # create button list container
        if self.item_list_container is not None:
            self.item_list_container.clear()
            if (self.item_list_container.relative_rect.width !=
                    (self.list_and_scroll_bar_container.relative_rect.width -
                     self.current_scroll_bar_width)):
                container_dimensions = (self.list_and_scroll_bar_container.relative_rect.width -
                                        self.current_scroll_bar_width,
                                        self.list_and_scroll_bar_container.relative_rect.height)
                self.item_list_container.set_dimensions(container_dimensions)
        else:
            self.item_list_container = UIContainer(
                pygame.Rect(0, 0,
                            self.list_and_scroll_bar_container.relative_rect.width -
                            self.current_scroll_bar_width,
                            self.list_and_scroll_bar_container.relative_rect.height),
                manager=self.ui_manager,
                starting_height=0,
                parent_element=self,
                container=self.list_and_scroll_bar_container,
                object_id='#item_list_container',
                anchors={'left': 'left',
                         'right': 'right',
                         'top': 'top',
                         'bottom': 'bottom'})
            self.join_focus_sets(self.item_list_container)
        item_y_height = 0
        for item in self.item_list:
            if item_y_height <= self.item_list_container.relative_rect.height:
                button_rect = pygame.Rect(0, item_y_height,
                                          self.item_list_container.relative_rect.width,
                                          self.list_item_height)
                item['button_element'] = UIButton(relative_rect=button_rect,
                                                  text=item['text'],
                                                  manager=self.ui_manager,
                                                  parent_element=self,
                                                  container=self.item_list_container,
                                                  object_id=ObjectID(
                                                      object_id=item['object_id'],
                                                      class_id='@selection_list_item'),
                                                  allow_double_clicks=self.allow_double_clicks,
                                                  anchors={'left': 'left',
                                                           'right': 'right',
                                                           'top': 'top',
                                                           'bottom': 'top'})
                self.join_focus_sets(item['button_element'])
                item_y_height += self.list_item_height
            else:
                break

    def remove_items(self, items_to_remove: Union[List[str], List[Tuple[str, str]]]) -> None:
        """
        Will remove all instances of the items provided. The full tuple is required for items with a
        display name and an object ID.

        :param items_to_remove: The list of new options to remove.
        """
        self._raw_item_list = [item for item in self._raw_item_list if item not in items_to_remove]
        self.set_item_list(self._raw_item_list)



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Options UI")
    resolution = (500, 400)

    display = pygame.display.set_mode(resolution)

    ui_manager = UIManager(resolution)
    ui_manager.set_window_resolution(resolution)
    ui_manager.clear_and_reset()

    background_surface = pygame.Surface(resolution)
    background_surface.fill(ui_manager.get_theme().get_colour('dark_bg'))
    UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 0, 50, 30), text='name', manager=ui_manager)
    UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 1, 50, 30), text='x', manager=ui_manager)
    UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 2, 50, 30), text='y', manager=ui_manager)
    UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 3, 50, 30), text='w', manager=ui_manager)
    UILabel(relative_rect=pygame.Rect(20, 50 + 30 * 4, 50, 30), text='h', manager=ui_manager)
    frame_name_entry_line = UITextEntryLine(relative_rect=pygame.Rect(70, 50, 180, 30), manager=ui_manager)
    frame_x_entry_line = UITextEntryLine(relative_rect=pygame.Rect(70, 50 + 30 * 1, 180, 30), manager=ui_manager)
    frame_y_entry_line = UITextEntryLine(relative_rect=pygame.Rect(70, 50 + 30 * 2, 180, 30), manager=ui_manager)
    frame_w_entry_line = UITextEntryLine(relative_rect=pygame.Rect(70, 50 + 30 * 3, 180, 30), manager=ui_manager)
    frame_h_entry_line = UITextEntryLine(relative_rect=pygame.Rect(70, 50 + 30 * 4, 180, 30), manager=ui_manager)
    # frame_data_entry_box = UITextEntryBox(relative_rect=pygame.Rect(10, 50, 200, 200), initial_text="",
    #                                       manager=ui_manager)
    frame_list = SelectionFrameList(
        relative_rect=pygame.Rect(260, 50, 200, 200),
        item_list=[('Item 1', (10, 20, 30, 20)),
                   ('Item 2', (10, 20, 30, 20))
                   ],
        manager=ui_manager
    )

    add_button = UIButton(relative_rect=pygame.Rect(10, 260, 75, 30),
                          text='Add', manager=ui_manager)
    save_button = UIButton(relative_rect=pygame.Rect(85, 260, 75, 30),
                           text='Save', manager=ui_manager)
    delete_button = UIButton(relative_rect=pygame.Rect(210, 260, 75, 30),
                             text='Delete', manager=ui_manager)

    clock = pygame.time.Clock()

    running = True
    while running:
        time_delta = clock.tick() / 1000.0
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            ui_manager.process_events(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == add_button:
                    name = frame_name_entry_line.get_text()
                    x = float(frame_x_entry_line.get_text())
                    y = float(frame_y_entry_line.get_text())
                    w = float(frame_w_entry_line.get_text())
                    h = float(frame_h_entry_line.get_text())
                    if name and x and y and w and h:
                        frame_list.add_items([(name, (x, y, w, h)), ])
                        frame_name_entry_line.set_text(f'{name[:-1]}{chr(ord(name[-1]) + 1)}')

                elif event.ui_element == delete_button:
                    selected_list = [item for item in frame_list.item_list if item['selected']]
                    if len(selected_list):  # ต้อง selected ให้มีข้อมูล
                        selected = selected_list[0]
                        frame_list.remove_items([(selected['text'], selected['frame_pos'])])
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
                selected_items = frame_list.get_single_selection()
                if selected_items:
                    selected_list = [item for item in frame_list.item_list if item['selected']]
                    if len(selected_list):  # ต้อง selected ให้มีข้อมูล
                        selected = selected_list[0]
                        frame_pos = selected['frame_pos']
                        x, y, w, h = frame_pos
                        frame_name_entry_line.set_text(selected['text'])
                        frame_x_entry_line.set_text(f'{x}')
                        frame_y_entry_line.set_text(f'{y}')
                        frame_w_entry_line.set_text(f'{w}')
                        frame_h_entry_line.set_text(f'{h}')

        ui_manager.update(time_delta)
        display.blit(background_surface, (0, 0))
        ui_manager.draw_ui(display)

        pygame.display.update()
