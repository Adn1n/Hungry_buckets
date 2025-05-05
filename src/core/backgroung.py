#
import pygame

class BackgroundManager:
    """
    Gère le fond d'écran : chargement, redimensionnement et affichage.
    """

    def __init__(self, image_path, width, height):
        self.original = pygame.image.load(image_path)
        self.current = pygame.transform.scale(self.original, (width, height))

    def resize(self, width, height):
        """Redimensionne l'image de fond quand la fenêtre est redimensionnée."""
        self.current = pygame.transform.scale(self.original, (width, height))

    def draw(self, surface):
        """Dessine l'image de fond sur la surface donnée."""
        surface.blit(self.current, (0, 0))