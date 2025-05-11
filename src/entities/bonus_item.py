import pygame
import random

class BonusItem:
    def __init__(self, image, screen_width):
        raw_img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(raw_img, (48, 48))  # ou (48, 48), à toi de choisir
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen_width - 50)
        self.rect.y = -self.rect.height  # spawn au-dessus de l’écran
        self.speed = 8

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self, screen_height):
        return self.rect.top > screen_height