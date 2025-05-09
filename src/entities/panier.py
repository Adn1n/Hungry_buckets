import pygame
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT

BASKET_WIDTH = 60
BASKET_HEIGHT = 10
BACKBOARD_WIDTH = 10
BACKBOARD_HEIGHT = 70

class Panier:
    def __init__(self):
        self.basket_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 200, BASKET_WIDTH, BASKET_HEIGHT)
        self.backboard_rect = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 250, BACKBOARD_WIDTH, BACKBOARD_HEIGHT)
        self.hoop_center_rect = pygame.Rect(self.basket_rect.centerx - 10, self.basket_rect.bottom, 20, 15)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 100, 100), self.basket_rect)        # Red for the rim
        pygame.draw.rect(screen, (100, 100, 100), self.backboard_rect)     # Grey for the backboard

    def get_rects(self):
        return self.backboard_rect, self.basket_rect, self.hoop_center_rect
