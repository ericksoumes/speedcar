import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Menu import Menu
from Code.RaceGame import RaceGame
from Code.Score import ScoreScreen


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # NEW GAME
                race_game = RaceGame(self.window)
                race_game.run()
            elif menu_return == MENU_OPTION[1]:  # SCORE
                score_screen = ScoreScreen(self.window)  # Agora não precisa de um `score`
                score_screen.show_high_scores()
            elif menu_return == MENU_OPTION[2]:  # EXIT
                pygame.quit()
                quit()
