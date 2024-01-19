


import pygame
import pygame_gui




class UIButton():
    def __init__(self, rect, img_path, manager):
        self.rect = rect
        self.img_path = img_path
        self.manager = manager
        self.image = pygame.image.load(self.img_path)

    def update(self, pos):
        if self.rect.collidepoint(pos):
            imagec = self.image.subsurface((0, 30, 45, 30))
            # Check for left mouse button click
            if pygame.mouse.get_pressed()[0]:
                print("Minimize button clicked!")
        else:
            imagec = self.image.subsurface((0, 0, 45, 30))
        image_element = pygame_gui.elements.UIImage(self.rect, imagec, self.manager)

pygame.init()

pygame.display.set_caption('Quick Start')
display = pygame.display.set_mode((1920, 1080))

background = pygame.Surface((1920, 1080))
background.fill((255, 255, 255))
tt_bar = pygame.Surface((1920, 30))
tt_bar.fill((204, 221, 236))

manager = pygame_gui.UIManager((1920, 1080))
minimize = UIButton(pygame.Rect((1920 - 45 * 3, 0), (45, 30)), 'UI/main button w/minimize.png', manager)
maximize = UIButton(pygame.Rect((1920 - 45 * 2, 0), (45, 30)), 'UI/main button w/maximize.png', manager)
close = UIButton(pygame.Rect((1920 - 45 * 1, 0), (45, 30)), 'UI/main button w/close.png', manager)

clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            is_running = False

    pos = pygame.mouse.get_pos()
    minimize.update(pos)
    maximize.update(pos)
    close.update(pos)

    display.blit(background, (0, 0))
    display.blit(tt_bar, (0, 0))
    manager.update(time_delta)
    manager.draw_ui(display)
    pygame.display.update()

pygame.quit()
