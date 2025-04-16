import math
import pygame

class Ball:
    def __init__(self, x, y, angle, force):
        self.x = x
        self.y = y
        self.radius = 20
        self.vx = force * math.cos(math.radians(angle)) * 1.2
        self.vy = -force * math.sin(math.radians(angle)) *1.2
        self.gravity = 0.5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Apply gravity

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius)
