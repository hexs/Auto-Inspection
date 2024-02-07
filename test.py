import pygame
from pygame.locals import *
import pygame_gui

pygame.init()

# Set up display
WINDOW_SIZE = (800, 600)
window_surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('UITextEntryLine Example')

# Create a UI manager
ui_manager = pygame_gui.UIManager(WINDOW_SIZE)

# Create a text entry line with default text "0"
text_entry_line = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 200), (400, 50)),
    manager=ui_manager,
)
text_entry_line.set_text('0')

# Main loop
is_running = True
clock = pygame.time.Clock()

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                mouse_pos = pygame.mouse.get_pos()
                if text_entry_line.rect.collidepoint(mouse_pos):
                    try:
                        current_text = int(text_entry_line.get_text())
                    except ValueError:
                        current_text = 0
                    text_entry_line.set_text(str(current_text + 1))
            elif event.button == 5:  # Mouse wheel down
                mouse_pos = pygame.mouse.get_pos()
                if text_entry_line.rect.collidepoint(mouse_pos):
                    try:
                        current_text = int(text_entry_line.get_text())
                    except ValueError:
                        current_text = 0
                    text_entry_line.set_text(str(current_text - 1))

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    window_surface.fill((255, 255, 255))
    ui_manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
