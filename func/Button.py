import pygame


class Button:
    def __init__(self, name, xywh, image_path=None, text=None, text_size=18, text_center='center'):
        self.name = name
        print(xywh)
        self.rect = pygame.Rect(*xywh)
        self.image_path = image_path
        self.text = text
        self.text_size = text_size
        self.text_center = text_center
        self.text_color = (255, 255, 255)
        self.update()

    def is_mouse_over(self, rect, mouse_pos):
        res = self.rect.move(rect.x, rect.y).collidepoint(mouse_pos)
        self.image = self.hover_image if res else self.default_image
        return res

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'text_color':
                self.text_color = v

        self.default_image = pygame.Surface(self.rect[2:], pygame.SRCALPHA)  # if mouse not on
        self.hover_image = pygame.Surface(self.rect[2:], pygame.SRCALPHA)  # if mouse on
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.default_image.blit(self.image, (0, 0), pygame.Rect(0, 0, *self.rect[2:]))
            self.hover_image.blit(self.image, (0, 0), pygame.Rect(0, self.rect[3], *self.rect[2:]))
            self.image = self.default_image

        if self.text:
            font = pygame.font.Font('ui/NotoSansThai.ttf', self.text_size)
            text_render = font.render(f'{self.text}', True, self.text_color)

            W, H = self.rect.size
            w, h = text_render.get_rect().size
            x, y = self.rect.center
            if self.text_center == 'center':
                x = W // 2 - w // 2
                y = H // 2 - h // 2
            if self.text_center == 'l':
                x = 0
                y = H // 2 - h // 2
            # print(x, y, w, h)
            # print()
            self.default_image.blit(text_render, (x - 1, y))
            self.hover_image.blit(text_render, (x, y + 1))
            # pygame.draw.rect(self.hover_image, (67, 69, 74), self.rect.move(-self.rect.x, -self.rect.y), 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
