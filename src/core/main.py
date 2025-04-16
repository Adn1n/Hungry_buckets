import pygame
from src.core.game import Game
from src.scenes.menu_screen import Menu

if __name__ == "__main__":
    pygame.init()  # Initialise les modules de Pygame

    game = Game()  # Crée une instance du jeu principal
    menu = Menu(game.ecran)  # Crée une instance du menu avec l’écran du jeu

    action = menu.handle()  # Affiche le menu et récupère l'action (ex : lancer le jeu)

    if game and action:  # Si une instance de jeu existe et que l'utilisateur a choisi de jouer, lancer le jeu
        game.run()
