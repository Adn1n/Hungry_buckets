import pygame
from game import Game
from menu_screen import Menu

if __name__ == "__main__":

    pygame.init()
    game = Game()
    menu = Menu(game.ecran)
    action = menu.handle()
    if game and action:
        game.run()
