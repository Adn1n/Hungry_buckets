import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASKET_COLOR = (255, 100, 100)
BACKBOARD_COLOR = (100, 100, 100)

PLAYER_Y = SCREEN_HEIGHT - 100
GRAVITY = 0.5


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "logo")