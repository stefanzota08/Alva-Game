import pygame
from .constants import RED, WHITE, BLUE, BLACK, GREEN, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.turn = True
        self.selected = None
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.color = WHITE
        self.opponent_color = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def highlight_piece(self, piece, row, col, turn):
        self.board.clear_selection()
        if turn == 1:
            piece.outline_color = GREEN
        else:
            piece.outline_color = RED
        self.selected = piece
        self.board.get_possible_moves(row, col, turn)
        print(self.board.possible_moves)

    def move_selected_piece(self):
        self.selected.PADDING = 100
        self.board.piece_map[self.selected.row][self.selected.col] = 0

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece != 0:
            if piece.PADDING == 30:
                if self.turn:  # daca e randul nostru
                    if piece.color != self.opponent_color:  # daca am apasat pe piesa noastra
                        self.highlight_piece(piece, row, col, 1)
                else:  # daca am apasat pe piesa adversarului
                    if piece.color == self.opponent_color:
                        self.highlight_piece(piece, row, col, 2)

            else:
                self.board.clear_selection()
                if self.turn:  # daca este randul nostru,
                    piece.color = self.color
                    if self.selected:
                        if (row, col) in self.board.possible_moves:
                            self.move_selected_piece()

                    # marcam piesa cu 1 in matrice
                    self.board.piece_map[row][col] = 1
                    self.turn = False
                    self.selected = None

                else:
                    # daca este randul oponentului, marcam piesa cu 2 in matrice
                    self.board.piece_map[row][col] = 2
                    piece.color = self.opponent_color
                    if self.selected:
                        if (row, col) in self.board.possible_moves:
                            self.move_selected_piece()

                    self.board.piece_map[row][col] = 2
                    self.turn = True
                    self.selected = None

                piece.PADDING = 30
            self.board.print_map()
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED