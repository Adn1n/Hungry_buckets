import os
import pygame
import math
import time

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
        self.ball_image = pygame.transform.scale(self.ball_image, (60, 60))  # Adjust size

    def update(self, gravity, screen_height, backboard_rect, basket_rect, hoop_center_rect):
        if not self.active:
            return

        # Appliquer gravité
        self.vel_y += gravity

        # Appliquer mouvement
        self.x += self.vel_x
        self.y += self.vel_y

        # Rebond au sol
        if self.y + 10 >= screen_height:
            self.y = screen_height - 10
            if abs(self.vel_y) > 1:
                self.vel_y *= -0.5
                self.vel_x *= 0.95
            else:
                self.vel_y = 0
                self.vel_x = 0
                if self.rest_time is None:
                    self.rest_time = time.time()

        # Rebond contre les bords de l’écran
        screen_width = 1000
        if self.x - 10 <= 0:
            self.x = 10
            self.vel_x *= -0.7
        elif self.x + 10 >= screen_width:
            self.x = screen_width - 10
            self.vel_x *= -0.7

        # Rebond contre la planche
        if self.rect().colliderect(backboard_rect):
            # Rebond horizontal
            if self.x < backboard_rect.left:
                self.x = backboard_rect.left - 10
            elif self.x > backboard_rect.right:
                self.x = backboard_rect.right + 10
            else:
                # Rebond vertical si touche par le dessous
                if self.y < backboard_rect.top:
                    self.y = backboard_rect.top - 10
                    self.vel_y *= -0.7
                else:
                    self.y = backboard_rect.bottom + 10
                    self.vel_y *= -0.7
            self.vel_x *= -0.7

        # Rebond contre l’anneau
        if self.rect().colliderect(basket_rect):
            if self.y < basket_rect.top:
                self.y = basket_rect.top - 10
                self.vel_y *= -0.5
            elif self.y > basket_rect.bottom:
                self.y = basket_rect.bottom + 10
                self.vel_y *= -0.5
            else:
                # Rebond latéral (côtés du cercle)
                if self.x < basket_rect.centerx:
                    self.x = basket_rect.left - 10
                else:
                    self.x = basket_rect.right + 10
                self.vel_x *= -0.6

        # Score : passe dans le centre du panier
        if self.rect().colliderect(hoop_center_rect):
            if self.vel_y > 0 and not self.scored:
                self.scored = True
                self.active = False
                return "score"
            elif self.vel_y < 0:  # remonte => pas un vrai panier
                self.active = False
                return

        # Désactivation après repos
        if self.rest_time and time.time() - self.rest_time >= 1.5:
            self.active = False

    def draw(self, screen):
        screen.blit(self.ball_image, (int(self.x) - 10, int(self.y) - 10))

    def rect(self):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)
