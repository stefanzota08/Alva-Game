import pygame

from .constants import RED, WHITE, BLUE, BLACK, GREEN, SQUARE_SIZE, GREY
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.turn = 1
        self.selected = None
        self.pieces_left = 34
        self.pieces_captured = 0
        self.opp_pieces_left = 34
        self.opp_pieces_captured = 0
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.color = WHITE
        self.opp_color = BLACK
        self.valid_moves = {}



    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def highlight_piece(self, row, col):
        self.selected = (row, col)
        selected_piece = self.board.get_piece(self.selected[0], self.selected[1])
        self.board.clear_selection()
        if self.turn == 1:
            selected_piece.outline_color = GREEN
        else:
            selected_piece.outline_color = RED
        self.board.get_possible_moves(row, col, self.turn)
        print(self.board.possible_moves)

    def remove_highlight(self):
        selected_piece = self.board.get_piece(self.selected[0], self.selected[1])
        selected_piece.outline_color = GREY
        self.selected = None

    def capture_pieces(self, row, col):
        # daca distanta e mai mare ca 1 sigur am capturat ceva
        captured = False
        if (abs(self.selected[0] - row) > 1 and abs(self.selected[0] - row) != 3) or (abs(self.selected[1] - col) > 1 and abs(self.selected[1] - col) != 3):
            print('capturam piese')
            if row != self.selected[0]:  # daca sunt diferite, mutarea a fost pe VERTICAL
                print('pe verticala')
                if row > self.selected[0]:
                    start = self.selected[0] + 1
                    end = row
                else:
                    start = row + 1
                    end = self.selected[0]
                for aux_row in range(start, end):
                    self.board.piece_map[aux_row][col] = 0
                    print('piesa gasita la ', aux_row, col)
                    if self.turn == 1:
                        self.pieces_captured += 1
                        self.opp_pieces_left -= 1
                        captured = True  # am capturat piese
                    else:
                        self.opp_pieces_captured += 1
                        self.pieces_left -= 1
                        captured = True  # am capturat piese

            elif col != self.selected[1]:  # daca sunt diferite, mutarea a fost pe ORIZONTAL
                print('pe orizontala')
                if col > self.selected[1]:
                    start = self.selected[1] + 1
                    end = col
                else:
                    start = col + 1
                    end = self.selected[1]
                print('de la ', start, 'pana la ', end-1)
                for aux_col in range(start, end):
                    self.board.piece_map[row][aux_col] = 0
                    if self.turn == 1:
                        self.pieces_captured += 1
                        self.opp_pieces_left -= 1
                        captured = True  # am capturat piese
                    else:
                        self.opp_pieces_captured += 1
                        self.pieces_left -= 1
                        captured = True  # am capturat piese
        return captured


    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


    def spawn_piece(self, row, col):
        self.board.piece_map[row][col] = self.turn
        self.change_turn()


    def move_selected_piece(self, row, col):
        if (row, col) in self.board.possible_moves:  # daca miscarea este posibila, mutam piesa
            print('move piece_map', self.selected[0], self.selected[1])
            print('pe locul', row, col)
            self.board.piece_map[self.selected[0]][self.selected[1]] = 0
            self.board.piece_map[row][col] = self.turn
            captured = self.capture_pieces(row, col)
            if not captured:  # daca nu a capturat, se termina tura, altfel ramane runda playerului curent
                print('nu a capturat nimic')
                self.remove_highlight()
                self.change_turn()
            else:
                self.highlight_piece(row, col)
        else:
            self.remove_highlight()


    def select(self, row, col):
        if self.board.piece_map[row][col] == self.turn:  # daca este randul nostru, selectam piesa
            self.highlight_piece(row, col)
            print('selected = ', self.selected[0], self.selected[1])
        elif self.board.piece_map[row][col] == 0:  # daca este liber locul selectat
            if self.selected:  # daca avem ceva selectat
                self.move_selected_piece(row, col)
            else:
                print('spawn')
                self.spawn_piece(row, col)
        self.board.print_map()
        self.board.update_UI()


    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
