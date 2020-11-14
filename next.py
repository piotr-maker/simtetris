from pygame import font, Surface, Rect
from os import path

from settings import Settings
from block import Block


class Next:
    MARGIN = 20
    FONT_SIZE = 34

    def __init__(self, offset = (0,0)):
        self.BG_COLOR = Settings.BG_COLOR
        self.BOARD_BG_COLOR = Settings.BOARD_BG_COLOR
        self.COLOR = Settings.COLOR
        self.SIDE = Settings.SQUARE_SIDE
        self.WIDTH = 4 * self.SIDE + 2 * self.MARGIN
        self.HEIGHT = self.WIDTH + self.FONT_SIZE

        font.init()
        self.font = font.Font(path.join('font','Teko-Regular.ttf'), self.FONT_SIZE)
        self.font_sf = self.font.render('Next', True, self.COLOR)
        self.rect = Rect(offset[0], offset[1], self.WIDTH, self.HEIGHT)


    def blit(self, screen, block):
        surface = Surface((self.WIDTH, self.HEIGHT))
        surface.fill(self.BG_COLOR)
        surface.blit(self.font_sf, self.font_sf.get_rect(center=(self.WIDTH//2, self.FONT_SIZE//2)))
        sf = Surface((self.WIDTH, self.HEIGHT - self.FONT_SIZE))
        sf.fill(self.BOARD_BG_COLOR)
        sf.get_rect(bottomleft=(surface.get_rect().bottomleft))

        x_offset = (self.WIDTH - block.cols * block.side) // 2
        y_offset = (self.HEIGHT - self.FONT_SIZE - block.rows * block.side) // 2 + block.rows * block.side

        block.blit(sf, (x_offset, y_offset))
        
        surface.blit(sf, sf.get_rect(bottomleft=(surface.get_rect().bottomleft)))

        screen.blit(surface, self.rect)
