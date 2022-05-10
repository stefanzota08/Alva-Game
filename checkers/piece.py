from .constants import RED, WHITE, SQUARE_SIZE, GREY, YELLOW
import pygame

class Piece:
    PADDING = 100
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.outline_color = GREY
        self.selected = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = (SQUARE_SIZE + 1) * self.col + SQUARE_SIZE + 1
        self.y = (SQUARE_SIZE + 1) * self.row + SQUARE_SIZE + 1

    
    def draw(self, win):
        radius = (SQUARE_SIZE + 1) // 2 - self.PADDING
        pygame.draw.circle(win, self.outline_color, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
