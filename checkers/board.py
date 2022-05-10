import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY, ROWS, COLS
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.piece_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.possible_moves = []
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS + 1):
            for col in range(COLS + 1):
                pygame.draw.rect(win, WHITE, (row * (SQUARE_SIZE + 1), col * (SQUARE_SIZE + 1), SQUARE_SIZE, SQUARE_SIZE))

    def print_map(self):
        for line in self.piece_map:
            print(line)
        print("\n")

    def get_possible_moves(self, row, col, turn):
        self.possible_moves = []
        # cautam prima pozite la dreapta
        _row = row
        _col = col
        while True:
            _col += 1
            if _col == -1 or _col == COLS or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if _col - col != 3:
                    self.possible_moves.append((_row, _col))
                    break
                else:
                    break

        # cautam prima pozite la stanga
        _row = row
        _col = col
        while True:
            _col -= 1
            if _col == -1 or _col == COLS or self.piece_map[_row][_col] == turn:
                break
            if self.piece_map[_row][_col] == 0:
                if col - _col != 3:
                    self.possible_moves.append((_row, _col))
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

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves