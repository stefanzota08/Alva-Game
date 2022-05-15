from copy import deepcopy
import pygame
import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(board, depth, turn):
    if depth == 0 or board.winner() is not None:
        return board.evaluate_2(turn), board

    if turn == 2:
        maxEval = float('-inf')
        best_move = None
        nodes = 0
        for move in get_all_moves(board, 2):
            nodes += 1
            evaluation = minimax(move, depth - 1, 1)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move, nodes
    else:
        minEval = float('inf')
        best_move = None
        nodes = 0
        for move in get_all_moves(board, 1):
            nodes += 1
            evaluation = minimax(move, depth - 1, 2)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move, nodes


def alpha_beta(board, depth, alpha, beta, turn):
    if depth == 0 or board.winner() is not None:
        return board.evaluate_2(turn), board

    if turn == 2:
        maxEval = float('-inf')
        best_move = None
        nodes = 0
        for move in get_all_moves(board, 2):
            nodes += 1
            evaluation = alpha_beta(move, depth - 1, alpha, beta, 1)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move, nodes

    else:
        minEval = float('inf')
        best_move = None
        nodes = 0
        for move in get_all_moves(board, 1):
            nodes += 1
            evaluation = alpha_beta(move, depth - 1, alpha, beta, 2)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_move = move
        return minEval, best_move, nodes


def simulate_move(piece, move, board, turn):
    all_possible_boards = []
    board.selected = piece  # setam piesa curenta ca fiind selectata
    if board.move_selected_piece(move[0], move[1], turn) and board.has_pieces_in_hand(turn):  # efectuam mutarea piesei la pozitia MOVE
        # daca returneaza True inseamna ca nu am capturat nimic, deci trebuie sa spawnam o piesa
        all_blank_spots = board.get_all_pieces(0)  # toate locurile goale
        for _ in range(4):
            aux_board = deepcopy(board)
            blank = random.choice(all_blank_spots)  # alegem un loc random in care sa spawnam piesa
            aux_board.spawn_piece(blank[0], blank[1])
            all_possible_boards.append(aux_board)  # adaugam tabla la lista cu toate tablele posibile
    else:  # daca a capturat, nu mai spawnam nimic
        all_possible_boards.append(board)

    return all_possible_boards

def simulate_spawn(board, turn):
    all_possible_spawns = []
    all_blank_spots = board.get_all_pieces(0)  # toate locurile goale
    for _ in range(4):
        aux_board = deepcopy(board)
        blank = random.choice(all_blank_spots)  # alegem un loc random in care sa spawnam piesa
        aux_board.spawn_piece(blank[0], blank[1])
        all_possible_spawns.append(aux_board)  # adaugam tabla la lista cu toate tablele posibile
    return all_possible_spawns


def get_all_moves(board, turn):
    moves = []
    pieces = board.get_all_pieces(turn)
    if not pieces:
        temp_board = deepcopy(board)
        new_boards = simulate_spawn(temp_board, turn)
        return new_boards
    else:
        for piece in pieces:  # iteram prin toate pozitiile pieselor cu valoarea = turn
            possible_moves, capturing_moves = board.get_possible_moves(piece[0], piece[1], turn)
            if not capturing_moves:
                valid_moves = possible_moves
            else:
                valid_moves = capturing_moves
            for move in valid_moves:
                temp_board = deepcopy(board)  # copiem tot obiectul BOARD, nu doar matricea
                temp_piece = deepcopy(piece)  # copiem pozitia piesei curente

                new_boards = simulate_move(temp_piece, move, temp_board, turn)
                # simulate_move intoarce toate variantele tablei posibile dupa mutarea pe pozitia salvata in move
                # pentru o pozitie facuta, daca nu a capturat nimic, va spawna piese in toate locurile posibile
                moves = moves + new_boards

            if not valid_moves:  # daca nu putem muta nicio piesa, spawnam una noua
                temp_board = deepcopy(board)
                new_boards = simulate_spawn(temp_board, turn)

                moves = moves + new_boards

    return moves
