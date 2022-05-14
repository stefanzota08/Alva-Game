from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(board, depth, max_player, game):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board.get_piece_map()

    if max_player:
        maxEval = float('-inf')
        best_move = []
        for move in get_all_moves(board, 2, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = []
        for move in get_all_moves(board, 1, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, turn, game):
    all_possible_boards = []
    board.selected = piece  # setam piesa curenta ca fiind selectata
    if board.move_selected_piece(move[0], move[1], turn):  # efectuam mutarea piesei la pozitia MOVE
        # daca returneaza True inseamna ca nu am capturat nimic, deci trebuie sa spawnam o piesa
        all_blank_spots = board.get_all_pieces(0)  # toate locurile goale
        for blank in all_blank_spots:
            aux_board = deepcopy(board)
            aux_board.spawn_piece(blank[0], blank[1])  # spawnam piesa pe fiecare loc in parte
            all_possible_boards.append(aux_board)  # adaugam tabla la lista cu toate tablele posibile
    else:  # daca a capturat, nu mai spawnam nimic
        all_possible_boards.append(board)

    return all_possible_boards


def get_all_moves(board, turn, game):
    moves = []
    pieces = board.get_all_pieces(turn)
    print('pozitiile pieselor cu numarul ', turn)
    print(pieces)
    for piece in board.get_all_pieces(turn):  # iteram prin toate pozitiile pieselor cu valoarea = turn
        possible_moves, capturing_moves = board.get_possible_moves(piece[0], piece[1], turn)
        if capturing_moves == []:
            valid_moves = possible_moves
        else:
            valid_moves = capturing_moves
        print('valid moves for piece ', piece[0], piece[1])
        print(valid_moves)
        print('simulam mutarile de mai sus pe rand')
        for move in valid_moves:
            print(move)
            temp_board = deepcopy(board)  # copiem tot obiectul BOARD, nu doar matricea
            temp_piece = deepcopy(piece)  # copiem pozitia piesei curente
            new_boards = simulate_move(temp_piece, move, temp_board, turn, game)
            # simulate_move intoarce toate variantele tablei posibile dupa mutarea pe pozitia salvata in move
            # pentru o pozitie facuta, daca nu a capturat nimic, va spawna piese in toate locurile posibile
            moves = moves + new_boards

    return moves
