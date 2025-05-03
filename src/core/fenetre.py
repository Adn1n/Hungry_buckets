import pygame
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Fenetre:
    def __init__(self, title="My Game", resizable=True):
        flags = pygame.RESIZABLE if resizable else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption(title)

    def get_screen(self):
        return self.screen

    def clear(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.flip()