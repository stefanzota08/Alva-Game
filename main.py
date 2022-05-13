# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
pygame.init()
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Alva')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y - 25) // (SQUARE_SIZE + 1)
    col = (x - 25) // (SQUARE_SIZE + 1)
    return row, col


def main():

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.board.p2_pieces_left == 1:
            value, new_board = minimax(game.get_board(), 4, 2, game)
            game.ai_move(new_board)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()

        game.update()
    
    pygame.quit()


main()
