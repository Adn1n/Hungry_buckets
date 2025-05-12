# Projet : Hungry Buckets
# Description : Ce fichier gère l'écran des options, avec affichage des boutons son, musique et retour.

import os
import pygame
from pygame import mouse

from hungry_goals.engine.config import *
from hungry_goals.utils import afficher_texte

####
class OptionScreen:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "options.png")
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.SysFont("arial", 20)

        # Rects cliquables (invisibles)
        self.sound_btn = pygame.Rect(320, 195, 320, 80)
        self.music_btn = pygame.Rect(320, 305, 320, 80)
        self.rules_btn = pygame.Rect(320, 415, 320, 80)
        self.back_btn = pygame.Rect(320, 515, 320, 60)  # ajuste selon la vraie position du bouton << BACK

    def draw(self,screen):
        """
        Affiche l'écran des options et retourne les zones cliquables.

        Paramètre:
            screen: surface Pygame où dessiner l'écran.

        Retour:
            sound_btn_rect, music_btn_rect, back_btn_rect: pygame.Rect des boutons cliquables.
        """
        # Affichage du fond
        img_option = self.background
        screen.blit(img_option, (0, 0))

        # Récupération des boutons cliquables
        sound_btn_rect = self.sound_btn
        music_btn_rect = self.music_btn
        back_btn_rect = self.back_btn
        rules_btn_rect = self.rules_btn


        return sound_btn_rect, music_btn_rect, back_btn_rect,rules_btn_rect
