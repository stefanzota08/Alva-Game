# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
import sys
import time
pygame.init()
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkers.game import Game
from minimax.algorithm import minimax, alpha_beta

FPS = 60


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Zota Stefan - Alva')

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y - 25) // (SQUARE_SIZE + 1)
    col = (x - 25) // (SQUARE_SIZE + 1)
    return row, col


def deseneaza_alegeri(display, tabla_curenta):

    btn_alg = GrupButoane(
        top=200,
        left=140,
        listaButoane=[
            Buton(display=display, w=300, h=50, text="minimax", valoare="minimax"),
            Buton(display=display, w=300, h=50, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=260,
        left=140,
        listaButoane=[
            Buton(display=display, w=300, h=50, text="alb", valoare="1"),
            Buton(display=display, w=300, h=50, text="negru", valoare="2")
        ],
        indiceSelectat=0)
    # am adaugat un buton pentru dificultate
    # 2. - dificultate
    btn_dif = GrupButoane(
        top=320,
        left=140,
        listaButoane=[
            Buton(display=display, w=196, h=50, text="usor", valoare="1"),
            Buton(display=display, w=196, h=50, text="mediu", valoare="2"),
            Buton(display=display, w=196, h=50, text="greu", valoare="3")
        ],
        indiceSelectat=0)

    # 13. - optiuni jucatori
    # am adaugat un buton pentru alegerea jucatorilor
    btn_tip_juc = GrupButoane(
        top=380,
        left=140,
        listaButoane=[
            Buton(display=display, w=196, h=50, text="P vs AI", valoare="1"),
            Buton(display=display, w=196, h=50, text="P vs P", valoare="2"),
            Buton(display=display, w=196, h=50, text="AI vs AI", valoare="3")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=440, left=320, w=250, h=50, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    btn_tip_juc.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if not btn_tip_juc.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.draw(display, 0)  # 0 pentru ca nu e niciun winner inca
                                    return btn_juc.getValoare(), btn_alg.getValoare(), btn_dif.getValoare(), btn_tip_juc.getValoare()
        pygame.display.update()


def main():

    game_time = time.time()
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    valori_meniu = deseneaza_alegeri(WIN, game.board)
    algorithm = valori_meniu[1]  # ce algoritm vom folosi
    player_turn = int(valori_meniu[0])  # ce rand va avea playerul (1 sau 2)
    dificultate = int(valori_meniu[2])  # dificultatea jocului (valori 1,2,4) = reprezinta adancimea in graf
    tip_joc = int(valori_meniu[3])  # 1 = player vs AI/ 2 = player vs player/ 3 = AI vs AI
    if player_turn == 1:
        AI_turn = 2
    else:
        AI_turn = 1
    
    AI_max_time = float('-inf')
    AI_min_time = float('inf')
    min_nodes = 0
    max_nodes = 0
    nr_mutari_AI = 0

    while run:
        clock.tick(FPS)

        if tip_joc == 1:

            if game.get_turn() == AI_turn:
                start_time = time.time()
                if algorithm == 'minimax':
                    value, new_board, nodes = minimax(game.get_board(), dificultate, AI_turn)
                    print("numar de noduri generate: ", nodes)
                    max_nodes = max(max_nodes, nodes)
                    min_nodes = min(min_nodes, nodes)
                    AI_time = float("{:.2f}".format(time.time() - start_time))
                    print('timp gandire AI: ', AI_time, 'sec')
                    print("estimare radacina arbore: ", value)
                    AI_max_time = max(AI_max_time, AI_time)
                    AI_min_time = min(AI_min_time, AI_time)
                    game.ai_move(new_board)
                    nr_mutari_AI += 1
                elif algorithm == 'alphabeta':
                    alpha = float('-inf')
                    beta = float('inf')
                    value, new_board, nodes = alpha_beta(game.get_board(), dificultate, alpha, beta, AI_turn)
                    print("numar de noduri generate: ", nodes)
                    max_nodes = max(max_nodes, nodes)
                    min_nodes = min(min_nodes, nodes)
                    AI_time = float("{:.2f}".format(time.time() - start_time))
                    print('timp gandire AI: ', AI_time, 'sec')
                    print("estimare radacina arbore: ", value)
                    AI_max_time = max(AI_max_time, AI_time)
                    AI_min_time = min(AI_min_time, AI_time)
                    game.ai_move(new_board)
                    nr_mutari_AI += 1


        elif tip_joc == 3:
            start_time = time.time()
            if algorithm == 'minimax':
                value, new_board, nodes = minimax(game.get_board(), dificultate, game.get_turn())
                print("numar de noduri generate: ", nodes)
                max_nodes = max(max_nodes, nodes)
                min_nodes = min(min_nodes, nodes)
                AI_time = float("{:.2f}".format(time.time() - start_time))
                print('timp gandire AI: ', AI_time, 'sec')
                print("estimare radacina arbore: ", value)
                AI_max_time = max(AI_max_time, AI_time)
                AI_min_time = min(AI_min_time, AI_time)
                game.ai_move(new_board)
                nr_mutari_AI += 1
            elif algorithm == 'alphabeta':
                alpha = float('-inf')
                beta = float('inf')
                value, new_board, nodes = alpha_beta(game.get_board(), dificultate, alpha, beta, game.get_turn())
                print("numar de noduri generate: ", nodes)
                max_nodes = max(max_nodes, nodes)
                min_nodes = min(min_nodes, nodes)
                AI_time = float("{:.2f}".format(time.time() - start_time))
                print('timp gandire AI: ', AI_time, 'sec')
                print("estimare radacina arbore: ", value)
                AI_max_time = max(AI_max_time, AI_time)
                AI_min_time = min(AI_min_time, AI_time)
                game.ai_move(new_board)
                nr_mutari_AI += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if tip_joc != 2:
                    # afisare maxim, minim si mediana - timp gandire
                    print('Timp minim gandire AI: ', AI_min_time)
                    print('Timp maxim gandire AI: ', AI_max_time)
                    print('Timp mediu gandire AI: ', (AI_min_time + AI_max_time) / 2)

                    # afisare maxim, minim, mediana - nr. noduri
                    print('Nr minim noduri: ', min_nodes)
                    print('Nr maxim noduri: ', max_nodes)
                    print('Nr mediu noduri: ', (min_nodes + max_nodes) // 2)
                    print('AI a efectuat in total: ', nr_mutari_AI, 'mutari')

                print('Jocul a rulat in total: ', time.time() - game_time, 'sec')
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
