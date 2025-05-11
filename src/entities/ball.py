import os
import pygame
import math
import time

from src.core.config import *
#


class Ball:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        self.vel_x = math.cos(angle) * power
        self.vel_y = math.sin(angle) * power
        self.active = True
        self.rest_time = None
        self.scored = False

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "Ball.png")



        self.ball_image = pygame.image.load(image_path)
        self.ball_image = pygame.transform.scale(self.ball_image, (50, 50))  # Adjust size to match original ball
        self.ball_radius = self.ball_image.get_width() // 2

    def update(self, gravity, screen_height, backboard_rect, basket_rect, hoop_center_rect):
        if not self.active:
            return

        self.vel_y += gravity
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y + self.ball_radius >= screen_height:
            self.y = screen_height - self.ball_radius
            if abs(self.vel_y) > 1:
                self.vel_y *= -0.5
                self.vel_x *= 0.95
            else:
                self.vel_y = 0
                self.vel_x = 0
                if self.rest_time is None:
                    self.rest_time = time.time()

        # Rebond côté gauche
        if self.x - self.ball_radius <= 0:
            self.x = self.ball_radius
            self.vel_x *= -0.8  # rebond plus doux
            self.vel_y *= 0.95  # légère perte d’énergie

        # Rebond côté droit
        elif self.x + self.ball_radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.ball_radius
            self.vel_x *= -0.8
            self.vel_y *= 0.95

        # Collision avec les bords de l'écran
        if self.x - 10 <= 0 or self.x + 10 >= 1000:
            self.vel_x *= -0.6

        if self.rect().colliderect(backboard_rect):
            self.x -= self.vel_x
            self.vel_x *= -0.7
        if self.rect().colliderect(basket_rect):
            self.x -= self.vel_x
            self.vel_x *= -0.6
        if self.rect().colliderect(hoop_center_rect) and self.vel_y > 0 and not self.scored:
            self.active = False
            self.scored = True
            return "score"

        # Si la balle vient d’en dessous et touche le fond du cerceau, on l’annule
        if self.rect().colliderect(hoop_center_rect) and self.vel_y < 0:
            self.active = False
            return

        if self.rest_time and time.time() - self.rest_time > 1.5:
            self.active = False





    def draw(self, screen):
        screen.blit(self.ball_image, (int(self.x - self.ball_radius), int(self.y - self.ball_radius)))

    def rect(self):
        return pygame.Rect(self.x - self.ball_radius, self.y - self.ball_radius, self.ball_radius * 2, self.ball_radius * 2)