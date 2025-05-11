#
import pygame

class BackgroundManager:
    """
    Gère le fond d'écran : chargement, redimensionnement et affichage.
    """

    def __init__(self, image_path, width, height):

        # Charge l'image à partir du chemin donné
        self.original = pygame.image.load(image_path)
        # Redimensionne l'image chargée aux dimensions spécifiées
        self.current = pygame.transform.scale(self.original, (width, height))

    def resize(self, width, height):
        """Redimensionne l'image de fond quand la fenêtre est redimensionnée."""

        # Met à jour l'image redimensionnée en fonction des nouvelles dimensions
        self.current = pygame.transform.scale(self.original, (width, height))

    def draw(self, surface):
        """Dessine l'image de fond sur la surface donnée."""

        # Affiche l'image redimensionnée sur la surface spécifiée à la position (0,0)
        surface.blit(self.current, (0, 0))