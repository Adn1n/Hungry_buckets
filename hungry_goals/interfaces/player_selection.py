# Projet : Hungry Buckets
# Description : Gère l’écran de sélection du joueur (affichage du fond et détection des clics sur les zones interactives).

import os
import pygame

from hungry_goals.engine.window import Fenetre
from hungry_goals.utils import *
from hungry_goals.engine.config import *

#
class ChoixJoueur():
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "choix_joueur1.png")
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.SysFont("arial", 20)

        self.btn_rect_axel = pygame.Rect(555, 160, 275, 345)
        self.btn_rect_tyson = pygame.Rect(160, 160, 280, 345)
        self.btn_rect_retour = pygame.Rect(50, 40, 195, 50)


    def draw(self,screen):
        """
        Affiche l'écran de choix du joueur et retourne les zones cliquables.

        Paramètres :
            screen : surface Pygame sur laquelle dessiner l'écran.

        Retour :
            tuple : (btn_axel, btn_tyson, btn_retour) - les Rects représentant les zones de clic pour Axel, Tyson et Retour.
        """
        # Affichage du fond
        img_option = self.background
        screen.blit(img_option, (0, 0))

        # Définition des boutons interactifs
        btn_axel = self.btn_rect_axel
        btn_tyson = self.btn_rect_tyson
        btn_retour = self.btn_rect_retour

        # Retour des zones cliquables
        return btn_axel, btn_tyson, btn_retour