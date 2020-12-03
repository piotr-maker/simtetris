from pygame import image, Surface, Rect
from os import path, getenv

from .settings import Settings


class Board:
    """ class holds current state of board """
    def __init__(self, offset=(0, 0)):
        self.BG_COLOR = Settings.BOARD_BG_COLOR
        self.ROWS = Settings.ROWS
        self.COLS = Settings.COLS
        self.OFFSET_X = offset[0]
        self.OFFSET_Y = offset[1]

        root = getenv('SNAP')
        square_img_path = path.join(root, 'graphics', 'gray.png') 
        self.image = image.load(square_img_path)
        self.SIDE = self.image.get_rect().width

        self.HEIGHT = self.ROWS * self.SIDE
        self.WIDTH = self.COLS * self.SIDE

        self.arr = list()
        self.reset()
        self.rect = Rect(self.OFFSET_X, self.OFFSET_Y, self.WIDTH, self.HEIGHT)

    def surface(self):
        """ return board surface """
        board = Surface(self.rect.size)
        board.fill(self.BG_COLOR)
        rect = self.image.get_rect()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.arr[row][col]:
                    rect.y = (self.ROWS - row - 1) * self.SIDE
                    rect.x = col * self.SIDE
                    board.blit(self.image, rect)

        return board

    def reset(self):
        """ reset board """
        self.arr = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS+4)]

    def add_block(self, block, row):
        """ add block to rest of the board and return how many rows removed
        or -1 if game over """
        col = block.column
        ri = row
        for r in range(block.rows):
            for c in range(block.cols):
                if ri + r >= self.ROWS:
                    return -1
                self.arr[ri + r][col + c] = self.arr[ri + r][col + c] or block.array[r][c]
        return self.check_filled((row, row + block.rows))

    def check_filled(self, row_range):
        """ check rows in row_range if they are filled """
        to_remove = []

        for i in range(row_range[0], row_range[1]):
            filled = True
            for j in range(self.COLS):
                if not self.arr[i][j]:
                    filled = False
                    break
            if filled:
                to_remove.append(i)

        self.remove_filled(to_remove)
        return len(to_remove)

    def remove_filled(self, rows):
        """ remove filled rows, update columns heights """
        for row in sorted(rows, reverse=True):
            for c in range(self.COLS):
                for r in range(row, self.ROWS - 1):
                    self.arr[r][c] = self.arr[r+1][c]
                self.arr[self.ROWS-1][c] = 0
