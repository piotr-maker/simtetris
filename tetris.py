import pygame
from random import randint
from os import path

from block import Block
from board import Board
from settings import Settings
from next import Next


class Tetris:
    high_score = 0
    level = 1

    # delay move when holding left or right button
    mov_delay = 5

    # how many lines to level up
    lev_up = 10


    def __init__(self):
        pygame.init()
        self.MARGIN = Settings.MARGIN
        self.COLOR = Settings.COLOR
        self.MESSAGE_BG_COLOR = (0, 0, 0)
        self.BG_COLOR = Settings.BG_COLOR
        self.SQUARE_SIDE = Settings.SQUARE_SIDE
        self.B_FONT_SIZE = 34
        self.MESSAGE_FONT = 26
        self.S_FONT_SIZE = 20
        self.MAX_LEVEL = Settings.MAX_LEVEL
        self.TURBO_SPEED = Settings.TURBO_SPEED
        self.FONT_NAME = 'Teko-Regular.ttf'

        self.board = Board((self.MARGIN,0))
        self.next = Next((self.MARGIN * 2 + self.board.WIDTH , 5))

        self.WIDTH = 3 * self.MARGIN + self.board.WIDTH + self.next.WIDTH
        self.HEIGHT = self.board.HEIGHT + self.MARGIN 

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tetris")

        # sounds
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        pygame.init()
       
        self.block_sd = pygame.mixer.Sound(path.join('sounds', 'block.wav'))
        self.pause_sd = pygame.mixer.Sound(path.join('sounds', 'pause.wav'))
        self.game_over_sd = pygame.mixer.Sound(path.join('sounds', 'game_over.wav'))
        self.level_up_sd = pygame.mixer.Sound(path.join('sounds', 'line_up.wav'))

        # fonts
        pygame.font.init()
        self.b_font = pygame.font.Font(path.join('font',self.FONT_NAME), self.B_FONT_SIZE)
        self.m_font = pygame.font.Font(path.join('font',self.FONT_NAME), self.MESSAGE_FONT)
        self.s_font = pygame.font.Font(path.join('font',self.FONT_NAME), self.S_FONT_SIZE)
        self.clock = pygame.time.Clock()

    
    def run_game(self):
        """ game main loop """
        self.reset()
        while self.run:
            self.check_events()
            self.repeat_mov_block()
            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)


    def repeat_mov_block(self):
        """ repeat moving with delay if key is pressed """
        if self.mov_r_timer:
            self.mov_r_timer -= 1
        elif self.mov_l_timer:
            self.mov_l_timer -= 1

        if self.mov_r_timer == 1:
            self.block.move_right(self.board.array)
            self.mov_r_timer = self.mov_delay
        elif self.mov_l_timer == 1:
            self.block.move_left(self.board.array)
            self.mov_l_timer = self.mov_delay
        


    def update_screen(self):
        self.screen.fill(self.BG_COLOR)
        sf = self.board.surface()
        self.block.blit(sf)
        if self.pause:
            self.draw_message(sf, 'PAUSE')
        if self.game_over:
            self.draw_message(sf, 'GAME OVER')
        self.screen.blit(sf, self.board.rect)
        self.next.blit(self.screen, self.next_block)
        if not (self.pause or self.game_over):
            self.block.y += self.speed
            self.block_collision()
        
        self.print_strings()


    def reset(self):
        """ reset the game """
        self.board.reset()
        self.run = True
        self.next_block = self.pick_block()
        self.block = self.pick_block()
        self.mov_r_timer = 0
        self.mov_l_timer = 0
        self.pause = False
        self.lines = 0
        self.score = 0
        self.level = 1
        self.game_over = False


    def block_collision(self):
        """ check if block will stop and wich row """
        collide = False
        col = self.block.column
        row = self.block.get_row()

        if row < 0:
            collide = True
        else:
            for i in range(self.block.cols):
                index = 0
                while not self.block.array[index][i]:
                    index += 1

                if row + index < self.board.ROWS:
                    if self.board.array[row + index][col + i]:
                        collide = True
                        break

        if collide:
            lines = self.board.add_block(self.block, row + 1)
            self.block = self.next_block
            self.next_block = self.pick_block()
            if lines == -1:
                # game over
                self.game_over_sd.play()
                self.game_over = True
                self.pause = True
            elif lines > 0:
                self.level_up_sd.play()
                self.lines += lines
                self.score += self.level * lines * lines * 10
                if self.score > self.high_score:
                    self.high_score = self.score
                if self.level < self.MAX_LEVEL:
                    self.level = self.lines // self.lev_up + 1
                    self.block_speed()
            else:
                self.block_sd.play()



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not self.game_over:
                        self.pause ^= 1
                        self.mov_r_timer = 0
                        self.mov_l_timer = 0
                        if self.pause:
                            self.pause_sd.play()
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_q:
                    self.run = False
                else:
                    if not self.pause:
                        if event.key == pygame.K_SPACE:
                            self.block.rotate(self.board.array)
                        elif event.key == pygame.K_RIGHT:
                            self.block.move_right(self.board.array)
                            self.mov_r_timer = 3 * self.mov_delay
                        elif event.key == pygame.K_LEFT:
                            self.block.move_left(self.board.array)
                            self.mov_l_timer = 3 * self.mov_delay
                        elif event.key == pygame.K_DOWN:
                            self.block_speed(True)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.block_speed()
                elif event.key == pygame.K_RIGHT:
                    self.mov_r_timer = 0
                elif event.key == pygame.K_LEFT:
                    self.mov_l_timer = 0


    def print_strings(self):
        """ print score, high score, press p to pause """
        x_offset = 2 * self.MARGIN + self.board.WIDTH
        y_offset = self.next.HEIGHT + self.MARGIN
        field = [ 
            { 'name': 'High Score', 'value': str(self.high_score)}, 
            { 'name': 'Score', 'value': str(self.score)},
            { 'name': 'Level', 'value': str(self.level)}, 
        ]

        for f in field:
            text = self.b_font.render( f['name'], True, self.COLOR )
            self.screen.blit(text, (x_offset, y_offset))
            y_offset += self.B_FONT_SIZE
            text = self.b_font.render( f['value'], True, self.COLOR )
            self.screen.blit(text, (x_offset, y_offset))
            y_offset += self.B_FONT_SIZE + self.MARGIN

        text = self.s_font.render( 'press p to pause', True, self.COLOR )
        x_offset = self.board.WIDTH +self.MARGIN + text.get_rect().width // 2
        y_offset = self.HEIGHT - self.MARGIN - self.S_FONT_SIZE
        self.screen.blit(text, (x_offset, y_offset))



    def draw_message(self, surface, message):
        """ draw message on middle of board """
        padding = 10
        text = self.m_font.render(message, True, self.COLOR)
        rect = text.get_rect(center=(self.board.WIDTH // 2, self.board.HEIGHT // 2))
        bg_rect = rect.copy()
        bg_rect.x -= padding
        bg_rect.y -= padding
        bg_rect.size = ( rect.width + 2 * padding, rect.height + 2 * padding )

        bg = pygame.Surface(bg_rect.size)
        bg.fill(self.MESSAGE_BG_COLOR)
        
        surface.blit(bg, bg_rect)
        surface.blit(text, rect)
        


    def block_speed(self, turbo = False):
        """ set block speed """
        self.speed = self.TURBO_SPEED if turbo else 0.6 + 0.3 * self.level


    def pick_block(self):
        """ pick random block """
        size = len(Block.BLOCKS)
        block = Block(randint(0, size-1 ))
        for _ in range(randint(0, 3)):
            block.rotate(self.board.array)
        self.block_speed()

        # turn off right and left move
        self.mov_r_timer = 0
        self.mov_l_timer = 0
        return block


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run_game()
