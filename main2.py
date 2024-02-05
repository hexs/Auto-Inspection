from typing import Union, List, Tuple, Optional, Dict
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface, UIElement, ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UISelectionList, UIButton, UIPanel, UITextEntryBox
import pygame
import pygame_gui


class FrameList(UISelectionList):
    def __init__(self,
                 relative_rect: pygame.Rect,
                 item_dict,
                 manager: Optional[IUIManagerInterface] = None,
                 *,
                 allow_multi_select: bool = False,
                 allow_double_clicks: bool = True,
                 container: Optional[IContainerLikeInterface] = None,
                 starting_height: int = 1,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,
                 default_selection: Optional[Union[
                     str, Tuple[str, str],  # Single-selection lists
                     List[str], List[Tuple[str, str]]  # Multi-selection lists
                 ]] = None,
                 ):
        item_list = list(item_dict.keys())
        super().__init__(relative_rect,
                         item_list,
                         manager,
                         allow_multi_select=allow_multi_select,
                         allow_double_clicks=allow_double_clicks,
                         container=container,
                         starting_height=starting_height,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible,
                         default_selection=default_selection
                         )
        self.item_dict = item_dict

    def update(self, time_delta: float):
        if self.scroll_bar is not None and self.scroll_bar.check_has_moved_recently():
            list_height_adjustment = min(self.scroll_bar.start_percentage *
                                         self.total_height_of_list,
                                         self.lowest_list_pos)
            for index, item in enumerate(self.item_list):
                print(item)
                new_height = int((index * self.list_item_height) - list_height_adjustment)
                if (-self.list_item_height <= new_height <= self.item_list_container.relative_rect.height):
                    if item['button_element'] is not None:
                        item['button_element'].set_relative_position((0, new_height))
                    else:
                        button_rect = pygame.Rect(0,
                                                  new_height,
                                                  self.item_list_container.relative_rect.width,
                                                  self.list_item_height)
                        button = UIButton(relative_rect=button_rect,
                                          text=item['text'],
                                          manager=self.ui_manager,
                                          parent_element=self,
                                          container=self.item_list_container,
                                          object_id=ObjectID(object_id=item['object_id'],
                                                             class_id='@selection_list_item'),
                                          allow_double_clicks=self.allow_double_clicks,
                                          anchors={'left': 'left',
                                                   'right': 'right',
                                                   'top': 'top',
                                                   'bottom': 'top'})
                        self.join_focus_sets(button)
                        item['button_element'] = button
                        if item['selected']:
                            item['button_element'].select()
                else:
                    if item['button_element'] is not None:
                        item['button_element'].kill()
                        item['button_element'] = None


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Options UI")
    resolution = (800, 600)

    window_surface = pygame.display.set_mode(resolution)

    ui_manager = UIManager(resolution)
    ui_manager.set_window_resolution(resolution)
    ui_manager.clear_and_reset()

    background_surface = pygame.Surface(resolution)
    background_surface.fill(ui_manager.get_theme().get_colour('dark_bg'))

    selection_list = FrameList(pygame.Rect(10, 50, 200, 200), item_dict={
        'Item 1': {},
        'Item 2': {}
    },
                               manager=ui_manager)

    text_entry_box = UITextEntryBox(
        relative_rect=pygame.Rect(210, 50, 200, 200),
        initial_text="",
        manager=ui_manager)

    add_button = UIButton(relative_rect=pygame.Rect(10, 260, 80, 30),
                          text='Add', manager=ui_manager)
    delete_button = UIButton(relative_rect=pygame.Rect(100, 260, 80, 30),
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
                    new_item = f'Item {len(selection_list.item_list) + 1}'
                    selection_list.add_items([new_item])
                elif event.ui_element == delete_button:
                    selected_items = selection_list.get_single_selection()
                    if selected_items:
                        print(selected_items)
                        selection_list.remove_items([selected_items])

            elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                selected_items = selection_list.get_single_selection()
                if selected_items:
                    text_entry_box.set_text(selected_items)

        ui_manager.update(time_delta)
        window_surface.blit(background_surface, (0, 0))
        ui_manager.draw_ui(window_surface)

        pygame.display.update()
