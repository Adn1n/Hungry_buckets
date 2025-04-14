import pygame
import math
from ball import Ball


class Arrow():

    def __init__(self, screen):
        self.screen = screen
        self.angle = 45  # angle de tir initial en degrés
        self.force = 10  # force du tir
        self.ball = None  # balle tirée

    def draw(self,ecran,joueur):
        arrow_length = 10 + self.force * 3
        rad = math.radians(self.angle)

        x_end = joueur.centerx + arrow_length * math.cos(rad)
        y_end = joueur.centery - arrow_length * math.sin(rad)

        pygame.draw.line(ecran, "white", joueur.center, (x_end, y_end), 8)

    def handle_events(self,joueur):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.angle +=  0.5
            if keys[pygame.K_RIGHT]:
                self.angle -=  0.5
            if keys[pygame.K_UP]:
                self.force += 1
            if keys[pygame.K_DOWN]:
                self.force = max(1, self.force - 1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.ball:
                    self.ball = Ball(joueur.centerx, joueur.centery, self.angle, self.force)


