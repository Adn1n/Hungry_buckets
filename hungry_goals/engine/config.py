import pygame
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600  # Dimensions de la fenêtre du jeu (largeur x hauteur)


WHITE = (255, 255, 255)  # Couleur blanche, utilisée pour les fonds ou textes clairs
BLACK = (0, 0, 0)        # Couleur noire, souvent pour le texte ou les contours
TEXT_COLOR = (0, 255, 255)  # Cyan clair (style rétro/néon) pour les textes visibles


BASKET_COLOR = (255, 100, 100)  # Couleur rouge clair pour le panier
BACKBOARD_COLOR = (100, 100, 100)  # Couleur grise pour le panneau du panier


PLAYER_Y = SCREEN_HEIGHT - 100  # Position verticale fixe du joueur (au sol)
GRAVITY = 0.5  # Force de gravité appliquée à la balle et autres objets


PLAYER_SPEED = 5  # Vitesse horizontale du joueur
ARCEAU_COLOR = (204, 0, 204)        # Couleur violet vif pour l'arceau (cerceau)
PANNEAU_COLOR = (46, 46, 184)  # Couleur bleue sombre pour le panneau


POINT_SCORE = 1  # Points gagnés par panier réussi
TEMPS_JEU = 45  # Durée du jeu en secondes

TEMPS_ADDITIONNEL = 3  # Temps supplémentaire accordé pour le bonus


font = pygame.font.SysFont(None, 36)    # Police de base pour les textes
font_big = pygame.font.SysFont(None, 48)    # Police plus grande pour titres ou scores
font_huge = pygame.font.SysFont(None, 120)    # Police très grande pour affichages importants


# Police style pixel art
pixel_font = pygame.font.Font(None, 48)


base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
image_path = os.path.join(base_path, "assets", "image", "Ball.png")

ball_image = pygame.image.load(image_path)
ball_image = pygame.transform.scale(ball_image, (50, 50))  # Ajuste la taille de la balle
BALL_RADIUS = ball_image.get_width() // 2  # Rayon de la balle utilisé pour la détection

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "logo")  # Dossier contenant le logo