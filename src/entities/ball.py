import math
import pygame
from src.core.config import *


class Ball:
    def __init__(self, x, y, angle, force,tir,sol):
        self.x = x  # Position horizontale initiale de la balle
        self.y = y  # Position verticale initiale de la balle
        self.radius = 20  # Rayon de la balle
        self.tir = tir
        self.sol = sol

        # Calcule la vitesse initiale en x et en y à partir de l'angle et de la force
        self.vx = force * math.cos(math.radians(angle)) * 0.3  # Vitesse horizontale
        self.vy = -force * math.sin(math.radians(angle)) * 0.3  # Vitesse verticale (négative car vers le haut)
        self.gravity = 8  # Gravité appliquée progressivement à la vitesse verticale
        print(f"vy: {self.vy}")

    def set_trajectoire(self, angle, force):
        self.vx = force * math.cos(math.radians(angle)) * 0.3
        self.vy = - force * math.sin(math.radians(angle)) * 0.3

    def update(self):
        print(f"gravity actuelle: {self.gravity}")
        if self.tir:

            self.vx *= 0.995
            self.vy += self.gravity
            self.vy *= 0.995

            # Debug après application complète
            print(f"vy final après gravité + air: {self.vy}")
            if self.vy > 0:
                print(">>> La balle redescend")
            else:
                print(">>> La balle monte toujours")

            # Corrige les blocages de la vitesse en tenant compte de la direction
            if abs(self.vy) < 0.1 and self.vy > 0:
                self.vy = 0

            # Mise à jour des positions
            self.x += self.vx
            self.y += self.vy

            print(f"y: {self.y}, vy: {self.vy}")

            # Rebond au sol
            if self.y + self.radius > self.sol:

                self.y = self.sol - self.radius
                self.vy *= -0.7
                # Stoppe si l'énergie est trop faible
                if abs(self.vy) < 0.5:
                    self.vy = 0
                    self.vx = 0
                    self.tir = False

            # Arrêt automatique si la balle est presque immobile
            if abs(self.vy) < 0.05 and abs(self.vx) < 0.05:
                self.vy = 0
                self.vx = 0
                self.tir = False

            # Empêche de sortir de l'écran horizontalement
            if self.x - self.radius < 0:
                self.x = self.radius
                self.vx *= -0.7
            elif self.x + self.radius > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.radius
                self.vx *= -0.7

            # Empêche la balle de sortir par le haut
            if self.y - self.radius < 0:
                self.y = self.radius
                self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius)
