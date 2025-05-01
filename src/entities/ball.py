import math
import pygame
from src.core.config import *
from src.core.config import *



class Ball:
    def __init__(self, x, y, angle, force,tir,sol):
        self.x = x  # Position horizontale initiale de la balle
        self.y = y  # Position verticale initiale de la balle

        self.sol = sol
        self.tir = tir

        self.gravity = 9.81 * 100  # pixels/s²
        self.speed = 20  # force du tir
        self.start_pos = (100, SCREEN_WIDTH - 100)
        self.ball_radius = 20

        # Convertir angle et vitesse en composantes vx et vy
        self.angle_rad = angle
        self.vx = self.speed * math.cos(self.angle_rad) * 50  # pixels/s
        self.vy = -self.speed * math.sin(self.angle_rad) * 50  # pixels/s

    def set_trajectoire(self, angle, force):
        self.vx = force * math.cos(math.radians(angle)) * 0.01
        self.vy = - force * math.sin(math.radians(angle)) * 0.01
        self.time_elapsed = 0

    def update(self, dt):
        print(f"gravity actuelle: {self.gravity}")
        if self.tir:
            self.time_elapsed += dt
            self.vy += self.vy * self.time_elapsed + 0.5 * self.gravity * self.time_elapsed ** 2
            self.vx *= dt


            print(f"vy final après gravité + air: {self.vy}")
            if self.vy > 0:
                print(">>> La balle redescend")
            else:
                print(">>> La balle monte toujours")


            print(f"y: {self.y}, vy: {self.vy}")

            if self.y + self.angle_rad > self.sol:
                self.y = self.sol - self.angle_rad
                self.vy *= -0.7
                if abs(self.vy) < 0.5:
                    self.vy = 0
                    self.vx = 0
                    self.tir = False

            if abs(self.vy) < 0.05 and abs(self.vx) < 0.05:
                self.vy = 0
                self.vx = 0
                self.tir = False

            if self.x - self.angle_rad < 0:
                self.x = self.angle_rad
                self.vx *= -0.7
            elif self.x + self.angle_rad > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.angle_rad
                self.vx *= -0.7

            if self.y - self.angle_rad < 0:
                self.y = self.angle_rad
                self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.ball_radius)
