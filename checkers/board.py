
import copy
import pygame
import math
pygame.init()
from .constants import BLACK, SQUARE_SIZE, WHITE, GREY, ROWS, COLS, GREEN, RED, WIDTH, HEIGHT
from .piece import Piece

class Board:
    def __init__(self):
        self.player_time = 0
        self.board = []
        self.piece_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.possible_moves = []
        self.capturing_moves = []
        self.turn = 1
        self.selected = None
        self.cant_select_pieces = False
        self.p1_pieces_left = 34
        self.p1_pieces_in_hand = 34
        self.p1_pieces_captured = 0
        self.p2_pieces_left = 34
        self.p2_pieces_in_hand = 34
        self.p2_pieces_captured = 0
        self.last_captured_nr = 0
        self.create_board()
    
    def draw_squares(self, win):
        pygame.init()
        win.fill(BLACK)
        # myfont = pygame.font.SysFont("monospace", 16)
        # disclaimertext = myfont.render("Copyright, 2013, Not Really Working Lamp Productions.", True, (0, 0, 0))
        # win.blit(disclaimertext, (5, 480))
        for row in range(ROWS + 1):
            for col in range(COLS + 1):
                pygame.draw.rect(win, WHITE, (row * (SQUARE_SIZE + 1), col * (SQUARE_SIZE + 1), SQUARE_SIZE, SQUARE_SIZE))

    def show_turn_on_screen(self, win):
        myfont = pygame.font.SysFont("arial", 16)
        if self.turn == 1:
            text = myfont.render("WHITE MOVES", True, (0, 0, 0))
        else:
            text = myfont.render("BLACK MOVES", True, (0, 0, 0))
        dreptunghi = pygame.Rect((SQUARE_SIZE, (COLS + 1) * SQUARE_SIZE + 30, SQUARE_SIZE * 2, SQUARE_SIZE // 2))

        # aici centram textul
        dreptunghiText = text.get_rect(center=dreptunghi.center)
        pygame.draw.rect(win, WHITE, dreptunghi)
        win.blit(text, dreptunghiText)

    def show_nr_of_pieces_on_screen(self, win):
        myfont = pygame.font.SysFont("arial", 16)
        text_white = myfont.render("White pieces left:" + str(self.p1_pieces_left), True, (0, 0, 0))
        text_black = myfont.render("Black pieces left:" + str(self.p2_pieces_left), True, (0, 0, 0))

        dreptunghi_white = pygame.Rect(350, 930, SQUARE_SIZE * 2, SQUARE_SIZE // 2)
        dreptunghi_black = pygame.Rect(600, 930, SQUARE_SIZE * 2, SQUARE_SIZE // 2)

        # aici centram textul
        dreptunghi_text_white = text_white.get_rect(center=dreptunghi_white.center)
        dreptunghi_text_black = text_black.get_rect(center=dreptunghi_black.center)
        pygame.draw.rect(win, WHITE, dreptunghi_white)
        pygame.draw.rect(win, WHITE, dreptunghi_black)
        win.blit(text_white, dreptunghi_text_white)
        win.blit(text_black, dreptunghi_text_black)

    def show_winner(self, win, winner):
        pygame.init()
        win.fill(BLACK)
        myfont = pygame.font.SysFont("arial", 50)
        if winner == 1:
            win.fill(WHITE)
            text = myfont.render("WHITE WON", True, (0, 0, 0))
        else:
            text = myfont.render("BLACK WON", True, (255, 255, 255))
        dreptunghi = pygame.Rect(0, 0, WIDTH, HEIGHT)

        # aici centram textul
        dreptunghiText = text.get_rect(center=dreptunghi.center)
        win.blit(text, dreptunghiText)
        self.turn = 3

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
        
    def draw(self, win, winner):
        self.draw_squares(win)
        self.show_turn_on_screen(win)
        self.show_nr_of_pieces_on_screen(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        if winner:
            self.show_winner(win, winner)

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
                elif self.piece_map[row][col] == '#':
                    piece.color = GREEN
                    piece.PADDING = 40
                    self.piece_map[row][col] = 0

    def get_all_pieces(self, turn):
        pieces = []
        for row_index in range(0, ROWS):
            for col_index in range(0, COLS):
                if self.piece_map[row_index][col_index] == turn:
                    pieces.append((row_index, col_index))
        return pieces
    
    def evaluate(self, turn):
        return self.p2_pieces_left - self.p1_pieces_left

    def evaluate_2(self, turn):
        return (self.p2_pieces_left - self.p1_pieces_left) * (self.p2_pieces_in_hand - self.p1_pieces_in_hand)

    def evaluate_3(self, turn):
        pieces = self.get_all_pieces(turn)
        if turn == 1:
            opp = self.get_all_pieces(2)
        else:
            opp = self.get_all_pieces(1)

        total_dist = 0
        nr = 0
        for piece in pieces:
            for opp_piece in opp:
                dist = math.dist(piece, opp_piece)
                total_dist += dist
                nr += 1

        total_dist = total_dist / nr

        return (self.p2_pieces_left - self.p1_pieces_left) * (self.p2_pieces_in_hand - self.p1_pieces_in_hand) * (total_dist * (-1))

    def winner(self):
        if self.p1_pieces_left == 0:
            return 'PLAYER 2 WON'
        if self.p2_pieces_left == 0:
            return 'PLAYER 1 WON'

    def highlight_valid_moves(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.piece_map[row][col] == '#':
                    self.piece_map[row][col] = 0

        if len(self.capturing_moves) > 0:
            for move in self.capturing_moves:
                self.piece_map[move[0]][move[1]] = '#'
        else:
            for move in self.possible_moves:
                self.piece_map[move[0]][move[1]] = '#'



    def highlight_piece(self, row, col):
        self.selected = (row, col)
        selected_piece = self.get_piece(self.selected[0], self.selected[1])
        self.clear_selection()
        if self.turn == 1:
            selected_piece.outline_color = GREEN
        else:
            selected_piece.outline_color = RED
        self.get_possible_moves(row, col, self.turn)
        self.highlight_valid_moves()
        # print('possible moves: ', self.possible_moves)
        # print('capturing moves: ', self.capturing_moves)
        
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
                    self.p1_pieces_in_hand += last_captured
                    self.p1_pieces_left += last_captured
                    self.p2_pieces_captured -= last_captured
                else:
                    # daca este randul adversarului, ii returnam piesele pierdute runda anterioara
                    # si le scadem din cele capturate de noi
                    self.p1_pieces_captured -= last_captured
                    self.p2_pieces_in_hand += last_captured
                    self.p2_pieces_left += last_captured

        return captured
    
    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def spawn_piece(self, row, col):
        if self.turn == 1:
            if self.p1_pieces_in_hand > 0:
                self.p1_pieces_in_hand -= 1  # daca mai avem piese in mana, scadem nr si spawnam
            else:
                return False  # daca nu mai avem piese de spawnat, nu putem spawna
        else:
            if self.p2_pieces_in_hand > 0:
                self.p2_pieces_in_hand -= 1  # daca mai avem piese in mana, scadem nr si spawnam
            else:
                return False  # daca nu mai avem piese de spawnat, nu putem spawna
        self.piece_map[row][col] = self.turn
        self.cant_select_pieces = False
        return True

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
                if (turn == 1 and self.p1_pieces_in_hand == 0) or (turn == 2 and self.p2_pieces_in_hand == 0):
                    self.change_turn()
                    self.cant_select_pieces = False
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
                self.print_map()
            else:
                if self.spawn_piece(row, col):  # daca returneaza True, am spawnat deci schimbam randul
                    self.print_map()
                    self.change_turn()
        self.update_UI()
        # print('we have ', self.p1_pieces_left, ' pieces left')
        # print('the opponent has ', self.p2_pieces_left, ' pieces left')

    def get_piece_map(self):
        return self.piece_map

    def update_stats(self, aux_board):
        self.piece_map = copy.deepcopy(aux_board.piece_map)
        self.p1_pieces_in_hand = aux_board.p1_pieces_in_hand
        self.p2_pieces_in_hand = aux_board.p2_pieces_in_hand
        self.p1_pieces_left = aux_board.p1_pieces_left
        self.p2_pieces_left = aux_board.p2_pieces_left
        self.p1_pieces_captured = aux_board.p1_pieces_captured
        self.p2_pieces_captured = aux_board.p2_pieces_captured
        self.last_captured_nr = aux_board.last_captured_nr
        self.print_map()

    def has_pieces_in_hand(self, turn):
        if turn == 1:
            return self.p1_pieces_in_hand > 0
        else:
            return self.p2_pieces_in_hand > 0
