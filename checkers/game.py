import pygame
from copy import deepcopy
from .constants import RED, WHITE, BLUE, BLACK, GREEN, SQUARE_SIZE, GREY
from checkers.board import Board

pygame.init()

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win, self.winner())
        pygame.display.update()

    def _init(self):
        self.board = Board()

    def winner(self):
        if self.board.p1_pieces_left == 0:
            return 2
        if self.board.p2_pieces_left == 0:
            return 1

    def reset(self):
        self._init()

    def highlight_piece(self, row, col):
        self.board.highlight_piece(row, col)

    def remove_highlight(self):
        self.board.remove_highlight()

    def capture_pieces(self, row, col):
        self.board.capture_pieces(row, col)

    def change_turn(self):
        self.board.change_turn()

    def spawn_piece(self, row, col):
        self.board.spawn_piece(row, col)

    def move_selected_piece(self, row, col, turn):
        self.board.move_selected_piece(row, col, turn)

    def select(self, row, col):
        self.board.select(row, col)

    def get_board(self):
        return self.board

    def ai_move(self, board):
        if not isinstance(board, list):
            self.change_turn()
            self.board.update_stats(board)
            self.board.update_UI()
        else:
            self.winner()

    def get_turn(self):
        return self.board.turn

    # def draw_valid_moves(self, moves):
    #     for move in moves:
    #         row, col = move
    #         pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
