from pygame import image, Surface, Rect
from os import path

from settings import Settings


class Block:
    BLOCKS = [
        { 'name': 'K', 'color': 'red', 'array': [ [1, 1], [1, 1] ] },
        { 'name': 'T', 'color': 'yellow', 'array': [ [1, 1, 1], [0, 1, 0] ] },
        { 'name': 'S', 'color': 'orange', 'array': [ [1, 1, 0], [0, 1, 1] ] },
        { 'name': 'Z', 'color': 'purple', 'array': [ [0, 1, 1], [1, 1, 0] ] },
        { 'name': 'L', 'color': 'green', 'array': [ [1, 1, 1], [ 1, 0, 0 ] ] },
        { 'name': 'J', 'color': 'green', 'array': [ [1, 1, 1], [ 0, 0, 1 ] ] },
        { 'name': 'I', 'color': 'blue', 'array': [ [1, 1, 1, 1] ] },
    ]

    def __init__(self, b_id):
        self.array = self.BLOCKS[b_id]['array']
        COLOR = self.BLOCKS[b_id]['color']
        self.name = self.BLOCKS[b_id]['name']
        self.BOARD_COLS = Settings.COLS
        self.BOARD_ROWS = Settings.ROWS

        self.image = image.load(path.join('graphics', COLOR + '.png'))
        self.side = self.image.get_rect().width
        self.y = 0
        self.column = Settings.COLS // 2 - 1
        
        self.rows = len(self.array)
        self.cols = len(self.array[0])


    def blit(self, surface, offset = None):
        """ draw block on surface """
        rect = self.image.get_rect()
        if offset == None:
            x_offset = self.column * self.side
            y_offset = self.y
        else:
            x_offset = offset[0]
            y_offset = offset[1]

        for i in range(self.rows):
            for j in range(self.cols):
                rect.x = x_offset + j * self.side
                rect.y = y_offset - (i + 1) * self.side
                if self.array[i][j]:
                    surface.blit(self.image, rect)


    def move_left(self, board_array):
        """ move block to the left """
        if self.column > 0:
            row = self.get_row()
            col = self.column
            able = True
        
            for r in range(self.rows):
                index = -1
                for c in range(self.cols):
                    if self.array[r][c]:
                        index += c
                        break
                if row + r < self.BOARD_ROWS and col + index > 0:
                    if board_array[row+r][col + index] or (board_array[row+r+1][col + index] and self.y % self.side < 20 ):
                        able = False
                        break
            if able:
                self.column -= 1


    def move_right(self, board_array):
        """ move block to the right """
        if self.column < self.BOARD_COLS - self.cols:
            row = self.get_row()
            able = True
        
            for r in range(self.rows):
                col = self.column + self.cols + 1
                for c in range(self.cols - 1, -1, -1):
                    col -= 1
                    if self.array[r][c]:
                        break
                if row + r < self.BOARD_ROWS:
                    if board_array[row+r][col] or (board_array[row+r+1][col] and self.y % self.side < 20 ):
                        able = False
                        break
            if able:
                self.column += 1


    def get_row(self):
        """ return in which row block is """
        return int((self.BOARD_ROWS * self.side - self.y) // self.side)


    def rotateable(self, board_array):
        """ check if piece can be rotated """
        row = self.get_row()
        width = self.rows
        left_space = [ 0 for _ in range(self.rows) ]
        right_space = [ 0 for _ in range(self.rows) ]

        for r in range(self.rows):
            col = self.column - 1
            while col >= 0 and not board_array[row+r][col]:
                left_space[r] += 1
                col -= 1

            col = self.column + self.cols
            while col < self.BOARD_COLS and not board_array[row+r][col]:
                right_space[r] += 1
                col += 1
            
        left_space = min(left_space)
        right_space = min(right_space)

        if left_space + right_space + self.cols >= width:
            if right_space < width - self.cols:
                self.column = self.column - width + self.cols + right_space
                if width == 4:
                    self.column += 1
            return True
        
        return False

    
    def rotate(self, board_array):
        """ rotate block 90 degrees right """
        if self.name != 'K' and self.rotateable(board_array):
            height = self.rows
            width = self.cols
            temp = []
        
            for v in self.array:
                temp += v

            self.array = [ [ temp[i+j*width] for j in range(height-1, -1, -1) ] for i in range(width) ]
            self.rows = width
            self.cols = height
        
            if self.cols == 4 and self.column != 0:
                self.column -= 1
            elif self.cols == 1:
                self.column += 1

            if self.column >= self.BOARD_COLS - self.cols:
                self.column = self.BOARD_COLS - self.cols
