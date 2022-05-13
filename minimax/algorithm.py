from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(board, depth, max_player, game):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board.get_piece_map()

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, 2, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, 1, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, game):
    board.selected = piece
    board.move_selected_piece(move[0], move[1])

    return board


def get_all_moves(board, turn, game):
    moves = []

    for piece in board.get_all_pieces(turn):  # iteram prin toate pozitiile pieselor cu valoarea = turn
        valid_moves = board.get_possible_moves(piece[0], piece[1], turn)

        for move in valid_moves.items():
            temp_board = deepcopy(board.piece_map)
            temp_piece = deepcopy(piece)
            new_board = simulate_move(temp_piece, move, temp_board, game)
            moves.append(new_board)

    return moves
