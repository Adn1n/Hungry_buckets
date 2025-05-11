import pygame
import random
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, BASKET_COLOR, BACKBOARD_COLOR, ARCEAU_COLOR, PANNEAU_COLOR


#
class Panier:
    def __init__(self):
        self.basket_rect = None
        self.backboard_rect = None
        self.hoop_center_rect = None
        self.direction = None
        self.repositionner()

    def draw(self, screen):
        pygame.draw.rect(screen, ARCEAU_COLOR, self.basket_rect)
        pygame.draw.rect(screen, PANNEAU_COLOR, self.backboard_rect)

    def repositionner(self):
        min_y = 200
        max_y = int(SCREEN_HEIGHT * 0.75)
        y = random.randint(min_y, max_y)

        basket_width = 70
        basket_height = 10
        backboard_width = 10
        backboard_height = 70
        hoop_width = 50
        hoop_height = 12

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