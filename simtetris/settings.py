from os import path, getenv

class Settings:
    # game
    MAX_LEVEL = 12
    TURBO_SPEED = 10

    # board
    ROWS = 20
    COLS = 13

    # block
    SQUARE_SIDE = 30

    # common
    COLOR = (255, 255, 255)
    BG_COLOR = (46, 44, 38)
    BOARD_BG_COLOR = (26, 26, 26)
    MARGIN = 20
    root = getenv('SNAP')
    FONT = path.join(root, 'fonts', 'Teko-Regular.ttf')
