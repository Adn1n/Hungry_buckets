import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 100, 255)
        self.speed = 5

    def handle_input(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        self.x = max(self.radius, min(screen_width - self.radius, self.x))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_position(self):
        return (self.x, self.y)