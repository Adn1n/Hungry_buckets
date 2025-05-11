# Hungry Buckets
# Description : Ce fichier gère l’affichage et le positionnement du panier dans le jeu.

import pygame
import random
import os
from hungry_goals.engine.config import SCREEN_WIDTH, SCREEN_HEIGHT, BASKET_COLOR, BACKBOARD_COLOR, ARCEAU_COLOR, PANNEAU_COLOR


#
class Panier:
    def __init__(self):
        self.basket_rect = None
        self.backboard_rect = None
        self.hoop_center_rect = None
        self.direction = None
        self.repositionner()

        filet_path = os.path.join("assets", "image", "filet.png")
        self.filet_image = pygame.image.load(filet_path).convert_alpha()
        self.filet_image = pygame.transform.scale(self.filet_image, (64, 36))  # adapte selon besoin

    def draw(self, screen):
        pygame.draw.rect(screen, ARCEAU_COLOR, self.basket_rect)
        filet_rect = self.filet_image.get_rect(midtop=(self.basket_rect.centerx - 4, self.basket_rect.bottom - 12))
        screen.blit(self.filet_image, filet_rect)

        pygame.draw.rect(screen, PANNEAU_COLOR, self.backboard_rect)

    def repositionner(self):
        """
        Repositionner dynamiquement le panier à une hauteur aléatoire.

        Aucun paramètre.

        Aucun retour.
        """
        # Calcul de la hauteur aléatoire du panier entre une valeur minimale et maximale
        y = random.randint(200, int(SCREEN_HEIGHT * 0.75))

        # Dimensions des différents éléments du panier
        basket_width = 70     # largeur de l'arceau (basket)
        basket_height = 4     # hauteur de l'arceau
        backboard_width = 10  # largeur du panneau (backboard)
        backboard_height = 70 # hauteur du panneau
        hoop_width = 50       # largeur de la zone centrale du panier (hoop)
        hoop_height = 12      # hauteur de la zone centrale du panier

        # Positionnement des rectangles représentant les différentes parties du panier
        self.basket_rect = pygame.Rect(SCREEN_WIDTH - 80, y, basket_width, basket_height)
        self.backboard_rect = pygame.Rect(
            self.basket_rect.right - backboard_width,
            self.basket_rect.top - backboard_height + 10,
            backboard_width,
            backboard_height
        )
        self.hoop_center_rect = pygame.Rect(
            self.basket_rect.centerx - hoop_width // 2,
            self.basket_rect.bottom,
            hoop_width,
            hoop_height
        )

    def move_horizontally(self):
        self.basket_rect.x += self.direction * 2
        if self.basket_rect.right > SCREEN_WIDTH or self.basket_rect.left < SCREEN_WIDTH // 2:
            self.direction *= -1

    def get_rects(self):
        return self.backboard_rect, self.basket_rect, self.hoop_center_rect