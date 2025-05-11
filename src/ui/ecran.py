# Projet : Hungry Goals
# Description : Gère les écrans intermédiaires comme l'écran de chargement (affichage, durée, barre de progression).

import pygame
import time

from src.utils import *
import os

#
class Ecran:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = screen.get_size()

    def show_loading_screen(self):
        """
        Affiche une image de chargement pendant un court délai avec une barre de progression.

        Aucun paramètre.

        Retourne rien.
        """

        # Chargement de l’image
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "chargement.png")
        loading_image = pygame.image.load(image_path)
        loading_image = pygame.transform.scale(loading_image, (self.WIDTH, self.HEIGHT))

        # Initialisation du temps et de la durée
        start_time = time.time()
        duration = 1 # secondes

        # Création de la police
        font = pygame.font.SysFont("arial", 30)

        # Boucle d’affichage
        while time.time() - start_time < duration:
            # Gestion des événements utilisateur
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE :
                        pygame.quit()
                        exit()

            # Affichage de l’image et de la barre de progression
            self.screen.fill((0, 0, 0))
            self.screen.blit(loading_image, (0, 0))

            progress = (time.time() - start_time) / duration
            progress_width = int(515 * progress)

            # barre de chargement
            pygame.draw.rect(self.screen, (255, 255, 255), (270, 515, 515, 15), 2)
            pygame.draw.rect(self.screen, (0, 255, 255), (270, 515, progress_width, 15))

            # Mise à jour de l’affichage et régulation du framerate
            pygame.display.flip()
            self.clock.tick(60)
