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
        self.gravity = 0.5  # Gravité appliquée progressivement à la vitesse verticale

    def set_trajectoire(self, angle, force):
        self.vx = force * math.cos(math.radians(angle)) * 0.3
        self.vy = -force * math.sin(math.radians(angle)) * 0.3

    def update(self):
        print("tir ?", self.tir)

        if self.tir:
            print(">>> balle en mouvement")
            # Met à jour la position de la balle selon sa vitesse
            self.x += self.vx
            self.y += self.vy

            # Applique la gravité à la vitesse verticale
            self.vy += self.gravity

        # Empêche la balle de sortir horizontalement
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius

        # Empêche la balle de sortir verticalement
        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > self.sol:
            self.y = self.sol - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius)

