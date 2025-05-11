# Projet : Hungry Buckets
# Description : Ce fichier définit la classe BonusItem, qui gère l’apparition, le mouvement et l’affichage des objets bonus dans le jeu.

import pygame
import random

class BonusItem:
    def __init__(self, image, screen_width):
        """
        Constructeur de la classe BonusItem.
        :param image: chemin vers l'image de l'objet bonus.
        :param screen_width: largeur de l'écran pour positionnement horizontal.
        Ne retourne rien.
        """
        raw_img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(raw_img, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -self.rect.height
        self.speed = 8

    def update(self):
        """
        Met à jour la position verticale de l'objet bonus.
        Ne prend pas de paramètre.
        Ne retourne rien.
        """
        self.rect.y += self.speed

    def draw(self, surface):
        """
        Dessine l'objet bonus sur la surface donnée.
        :param surface: surface pygame sur laquelle dessiner l'objet.
        Ne retourne rien.
        """
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self, screen_height):
        """
        Vérifie si l'objet bonus est sorti de l'écran.
        :param screen_height: hauteur de l'écran.
        :return: True si l'objet est hors écran, sinon False.
        """
        return self.rect.top > screen_height