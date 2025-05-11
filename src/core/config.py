import pygame
import os


pygame.init()
#
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (0, 255, 255)  # Cyan clair (style rétro/néon)

BASKET_COLOR = (255, 100, 100)
BACKBOARD_COLOR = (100, 100, 100)

PLAYER_Y = SCREEN_HEIGHT - 100
GRAVITY = 0.5


PLAYER_SPEED = 5
ARCEAU_COLOR = (204, 0, 204)        # Rouge vif
PANNEAU_COLOR = (46, 46, 184)


POINT_SCORE = 13
TEMPS_JEU = 15



font = pygame.font.SysFont(None, 36)    #
font_big = pygame.font.SysFont(None, 48)    #
font_huge = pygame.font.SysFont(None, 120)    #

# Police style pixel art (ex: pour le score affiché dans le menu)
pixel_font = pygame.font.Font(None, 48)  # Remplace None par le chemin si tu utilises une .ttf custom


base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
image_path = os.path.join(base_path, "assets", "image", "Ball.png")

ball_image = pygame.image.load(image_path)
ball_image = pygame.transform.scale(ball_image, (50, 50))  # Adjust size to match original ball
BALL_RADIUS = ball_image.get_width() // 2


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "logo")