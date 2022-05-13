import pygame

from .constants import RED, WHITE, BLUE, BLACK, GREEN, SQUARE_SIZE, GREY
from checkers.board import Board

pygame.init()

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    
    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.turn = 1
        self.selected = None
        self.cant_select_pieces = False
        self.p1_pieces_left = 34
        self.p1_pieces_captured = 0
        self.p2_pieces_left = 34
        self.p2_pieces_captured = 0
        self.last_captured_nr = 0


    def winner(self):
        if self.p1_pieces_left == 0:
            return 'PLAYER 2 WON'
        if self.p2_pieces_left == 0:
            return 'PLAYER 1 WON'

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
        print('possible moves: ', self.board.possible_moves)
        print('capturing moves: ', self.board.capturing_moves)

    def remove_highlight(self):
        selected_piece = self.board.get_piece(self.selected[0], self.selected[1])
        selected_piece.outline_color = GREY
        self.selected = None

    def capture_pieces(self, row, col):
        captured = False
        last_captured = self.last_captured_nr  # tinem minte cate s-au capturat ultima oara
        self.last_captured_nr = 0  # initializam cu 0 pentru a putea numara cate se captureaza acum

        # daca distanta e mai mare ca 1 sigur am capturat ceva
        if (abs(self.selected[0] - row) > 1 and abs(self.selected[0] - row) != 3) or (abs(self.selected[1] - col) > 1 and abs(self.selected[1] - col) != 3):
            if row != self.selected[0]:  # daca sunt diferite, mutarea a fost pe VERTICAL
                if row > self.selected[0]:
                    start = self.selected[0] + 1
                    end = row
                else:
                    start = row + 1
                    end = self.selected[0]

                for aux_row in range(start, end):
                    self.board.piece_map[aux_row][col] = 0
                    if self.turn == 1:
                        self.p1_pieces_captured += 1
                        self.last_captured_nr += 1
                        self.p2_pieces_left -= 1
                        captured = True  # am capturat piese
                    else:
                        self.p2_pieces_captured += 1
                        self.last_captured_nr += 1
                        self.p1_pieces_left -= 1
                        captured = True  # am capturat piese

            elif col != self.selected[1]:  # daca sunt diferite, mutarea a fost pe ORIZONTAL
                if col > self.selected[1]:
                    start = self.selected[1] + 1
                    end = col
                else:
                    start = col + 1
                    end = self.selected[1]
                for aux_col in range(start, end):
                    self.board.piece_map[row][aux_col] = 0
                    if self.turn == 1:
                        self.p1_pieces_captured += 1
                        self.p2_pieces_left -= 1
                        captured = True  # am capturat piese
                    else:
                        self.p2_pieces_captured += 1
                        self.p1_pieces_left -= 1
                        captured = True  # am capturat piese

            if last_captured == self.last_captured_nr and last_captured > 1:  # testam daca s-au capturat acelasi nr de piese ca runda anterioara
                if self.turn == 1:
                    # daca este randul nostru, ne recuperam piesele pierdute runda anterioara
                    # si le scadem din cele capturate de adversar
                    self.p1_pieces_left += last_captured
                    self.p2_pieces_captured -= last_captured
                else:
                    # daca este randul adversarului, ii returnam piesele pierdute runda anterioara
                    # si le scadem din cele capturate de noi
                    self.p1_pieces_captured -= last_captured
                    self.p2_pieces_left += last_captured

        return captured


    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


    def spawn_piece(self, row, col):
        self.board.piece_map[row][col] = self.turn
        self.cant_select_pieces = False
        self.change_turn()


    def move_selected_piece(self, row, col):
        # daca avem mutari in care putem captura, si aceasta nu e una din ele, dam return
        if (row, col) not in self.board.capturing_moves and len(self.board.capturing_moves) > 0:
            return
        if (row, col) in self.board.possible_moves:  # daca miscarea este posibila, mutam piesa
            self.board.piece_map[self.selected[0]][self.selected[1]] = 0
            self.board.piece_map[row][col] = self.turn
            captured = self.capture_pieces(row, col)
            if captured:  # daca a capturat, se termina tura
                self.board.get_possible_moves(row, col, self.turn)
                if len(self.board.capturing_moves) == 0:
                    self.remove_highlight()
                    self.change_turn()
            else:  # daca nu a capturat nimic, inseamna ca a mutat doar o casuta, deci mai poate sa si adauge o piesa
                self.remove_highlight()
                self.cant_select_pieces = True  # nu poate selecta alte piese, poate decat plasa o piesa
        else:
            self.remove_highlight()




    def select(self, row, col):
        if self.board.piece_map[row][col] == self.turn:  # testam daca piesa aleasa este a playerului curent
            if not self.cant_select_pieces:  # testam daca avem voie sa selectam piese
                self.highlight_piece(row, col)
        elif self.board.piece_map[row][col] == 0:  # daca este liber locul selectat
            if self.selected:  # daca avem ceva selectat
                self.move_selected_piece(row, col)
            else:
                self.spawn_piece(row, col)
        self.board.print_map()
        self.board.update_UI()
        print('we have ', self.p1_pieces_left, ' pieces left')
        print('the opponent has ', self.p2_pieces_left, ' pieces left')

    # def draw_valid_moves(self, moves):
    #     for move in moves:
    #         row, col = move
    #         pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
