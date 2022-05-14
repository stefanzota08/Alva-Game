import copy

import pygame
pygame.init()
from .constants import BLACK, SQUARE_SIZE, WHITE, GREY, ROWS, COLS, GREEN, RED
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.piece_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.possible_moves = []
        self.capturing_moves = []
        self.turn = 1
        self.selected = None
        self.cant_select_pieces = False
        self.p1_pieces_left = 4
        self.p1_pieces_captured = 0
        self.p2_pieces_left = 4
        self.p2_pieces_captured = 0
        self.last_captured_nr = 0
        self.create_board()
    
    def draw_squares(self, win):
        pygame.init()
        win.fill(BLACK)
        myfont = pygame.font.SysFont("monospace", 16)
        disclaimertext = myfont.render("Copyright, 2013, Not Really Working Lamp Productions.", True, (0, 0, 0))
        win.blit(disclaimertext, (5, 480))
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

        possible_moves_copy = copy.deepcopy(self.possible_moves)
        capturing_moves_copy = copy.deepcopy(self.capturing_moves)
        return possible_moves_copy, capturing_moves_copy

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

    def get_all_pieces(self, turn):
        pieces = []
        for row_index in range(0, ROWS):
            for col_index in range(0, COLS):
                if self.piece_map[row_index][col_index] == turn:
                    pieces.append((row_index, col_index))
        return pieces
    
    def evaluate(self):
        return self.p2_pieces_left - self.p1_pieces_left
    
    def winner(self):
        if self.p1_pieces_left == 0:
            return 'PLAYER 2 WON'
        if self.p2_pieces_left == 0:
            return 'PLAYER 1 WON'

    def highlight_piece(self, row, col):
        self.selected = (row, col)
        selected_piece = self.get_piece(self.selected[0], self.selected[1])
        self.clear_selection()
        if self.turn == 1:
            selected_piece.outline_color = GREEN
        else:
            selected_piece.outline_color = RED
        self.get_possible_moves(row, col, self.turn)
        print('possible moves: ', self.possible_moves)
        print('capturing moves: ', self.capturing_moves)
        
    def remove_highlight(self):
        selected_piece = self.get_piece(self.selected[0], self.selected[1])
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
                    self.piece_map[aux_row][col] = 0
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
                    self.piece_map[row][aux_col] = 0
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
        self.piece_map[row][col] = self.turn
        self.cant_select_pieces = False

    def move_selected_piece(self, row, col, turn):
        # daca avem mutari in care putem captura, si aceasta nu e una din ele, dam return
        if (row, col) not in self.capturing_moves and len(self.capturing_moves) > 0:
            return
        if (row, col) in self.possible_moves:  # daca miscarea este posibila, mutam piesa
            self.piece_map[self.selected[0]][self.selected[1]] = 0
            self.piece_map[row][col] = turn
            captured = self.capture_pieces(row, col)
            if captured:  # daca a capturat, se termina tura
                self.get_possible_moves(row, col, turn)
                if len(self.capturing_moves) == 0:
                    self.remove_highlight()
                    self.change_turn()
            else:  # daca nu a capturat nimic, inseamna ca a mutat doar o casuta, deci mai poate sa si adauge o piesa
                self.remove_highlight()
                self.cant_select_pieces = True  # nu poate selecta alte piese, poate decat plasa o piesa
                return True  # returnam True daca nu a capturat nimic
        else:
            self.remove_highlight()
        return None


    def select(self, row, col):
        if self.piece_map[row][col] == self.turn:  # testam daca piesa aleasa este a playerului curent
            if not self.cant_select_pieces:  # testam daca avem voie sa selectam piese
                self.highlight_piece(row, col)
        elif self.piece_map[row][col] == 0:  # daca este liber locul selectat
            if self.selected:  # daca avem ceva selectat
                self.move_selected_piece(row, col, self.turn)
            else:
                self.spawn_piece(row, col)
                self.change_turn()
        # self.print_map()
        self.update_UI()
        # print('we have ', self.p1_pieces_left, ' pieces left')
        # print('the opponent has ', self.p2_pieces_left, ' pieces left')

    def get_piece_map(self):
        return self.piece_map

    def update_piece_map(self, piece_map):
        self.piece_map = copy.deepcopy(piece_map)