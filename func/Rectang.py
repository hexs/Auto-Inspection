from func.TextColor import *


class Rectang:
    def __init__(self, x: float, y: float, dx: float, dy: float, shape=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.index__next__ = 0
        self.shape = shape

    def __str__(self):
        return (f'{UNDERLINE}{BOLD}{CYAN}{self.x}{ENDC}{UNDERLINE} {BOLD}{PINK}{self.y}{ENDC} -> '
                f'{UNDERLINE}{BOLD}{CYAN}{self.dx}{ENDC}{UNDERLINE} {BOLD}{PINK}{self.dy}{ENDC}')

    def __iter__(self):
        return self

    def __next__(self):
        self.index__next__ += 1
        if self.index__next__ == 1:
            return self.x
        elif self.index__next__ == 2:
            return self.y
        elif self.index__next__ == 3:
            return self.dx
        elif self.index__next__ == 4:
            return self.dy
        else:
            self.index__next__ = 0
            raise StopIteration

    def to_pix_xywh(self, **kwargs):
        if kwargs.get('shape'):
            self.shape = kwargs.get('shape')
        x = round((self.x - self.dx / 2) * self.shape[0])
        y = round((self.y - self.dy / 2) * self.shape[1])
        w = round(self.dx * self.shape[0])
        h = round(self.dy * self.shape[1])
        return x, y, w, h

    def to_pix_xyxy(self, **kwargs):
        if kwargs.get('shape'):
            self.shape = kwargs.get('shape')
        x1 = (self.x - self.dx / 2) * self.shape[0]
        y1 = (self.y - self.dy / 2) * self.shape[1]
        x2 = (self.x + self.dx / 2) * self.shape[0]
        y2 = (self.y + self.dy / 2) * self.shape[1]
        return x1, y1, x2, y2
