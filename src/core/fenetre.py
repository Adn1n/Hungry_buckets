import pygame
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
# Classe Fenetre : gère la fenêtre principale du jeu avec Pygame.
class Fenetre:
    def __init__(self, title="My Game", resizable=True):
        """
        Initialise la fenêtre du jeu.
        - title : le titre affiché dans la barre de la fenêtre.
        - resizable : permet de redimensionner la fenêtre si True.
        """
        # Détermine le drapeau pour rendre la fenêtre redimensionnable si demandé.
        flags = pygame.RESIZABLE if resizable else 0

        # Crée la fenêtre principale avec la largeur et hauteur définies dans la config.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        # Définit le titre de la fenêtre.
        pygame.display.set_caption(title)

    def get_screen(self):
        """
        Retourne la surface (screen) sur laquelle dessiner.
        Utile pour accéder à la fenêtre depuis d'autres classes.
        """
        return self.screen

    def clear(self, color):
        """
        Efface la fenêtre en la remplissant avec une couleur (tuple RGB).
        À appeler au début de chaque frame pour réinitialiser l'affichage.
        """
        self.screen.fill(color)

    def update(self):
        """
        Met à jour l'affichage de la fenêtre.
        À appeler à la fin de chaque frame pour afficher les dessins à l'écran.
        """
        pygame.display.flip()