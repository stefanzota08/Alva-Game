import pygame
pygame.init()
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY, ROWS, COLS
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.piece_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.possible_moves = []
        self.capturing_moves = []
        self.create_board()
    
    def draw_squares(self, win):
        pygame.init()
        win.fill(BLACK)
        myfont = pygame.font.SysFont("monospace", 16)
        disclaimertext = myfont.render("Copyright, 2013, Not Really Working Lamp Productions.", True, (0, 0, 0))
        win.blit(disclaimertext, (5, 480))
        print('text added')
        for row in range(ROWS + 1):
            for col in range(COLS + 1):
                pygame.draw.rect(win, WHITE, (row * (SQUARE_SIZE + 1), col * (SQUARE_SIZE + 1), SQUARE_SIZE, SQUARE_SIZE))

    def print_map(self):
        for line in self.piece_map:
            print(line)
        print("\n")

    def get_possible_moves(self, row, col, turn):
        self.possible_moves = []
        self.capturing_moves = []
        # cautam prima pozite la dreapta
        _row = row
        _col = col
        while True:
            _col += 1
            if _col == COLS or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if _col - col != 3:
                    self.possible_moves.append((_row, _col))
                    if _col - col != 1:
                        self.capturing_moves.append((_row, _col))
                    break
                else:
                    break
        # cautam prima pozite la stanga
        _row = row
        _col = col
        while True:
            _col -= 1
            if _col == -1 or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if col - _col != 3:
                    self.possible_moves.append((_row, _col))
                    if col - _col != 1:
                        self.capturing_moves.append((_row, _col))
                    break
                else:
                    break

        # cautam prima pozite in jos
        _row = row
        _col = col
        while True:
            _row += 1
            if _row == -1 or _row == ROWS or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if _row - row != 3:
                    self.possible_moves.append((_row, _col))
                    if _row - row != 1:
                        self.capturing_moves.append((_row, _col))
                    break
                else:
                    break

        # cautam prima pozitie in sus
        _row = row
        _col = col
        while True:
            _row -= 1
            if _row == -1 or _row == ROWS or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if row - _row != 3:
                    self.possible_moves.append((_row, _col))
                    if row - _row != 1:
                        self.capturing_moves.append((_row, _col))
                    break
                else:
                    break

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        # self.print_map()
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Piece(row, col, GREY))
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def clear_selection(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                piece.outline_color = GREY

    def update_UI(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if self.piece_map[row][col] == 1:
                    piece.color = WHITE
                    piece.PADDING = 30
                elif self.piece_map[row][col] == 2:
                    piece.color = BLACK
                    piece.PADDING = 30
                elif self.piece_map[row][col] == 0:
                    piece.color = GREY
                    piece.PADDING = 100
