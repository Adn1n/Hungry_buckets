import pygame
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BASKET_COLOR, BACKBOARD_COLOR

class Panier:
    def __init__(self):
        self.basket_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 200, 60, 10)
        self.backboard_rect = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 250, 10, 70)
        self.hoop_center_rect = pygame.Rect(self.basket_rect.centerx - 15, self.basket_rect.bottom, 30, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, BASKET_COLOR, self.basket_rect)
        pygame.draw.rect(screen, BACKBOARD_COLOR, self.backboard_rect)

    def get_rects(self):
        return self.backboard_rect, self.basket_rect, self.hoop_center_rect