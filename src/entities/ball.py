import pygame
import math
import time
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

        self.ball_image = pygame.image.load("assets/image/Ball.png")
        self.ball_image = pygame.transform.scale(self.ball_image, (60, 60))  # Adjust size to match original ball

    def update(self, gravity, screen_height, backboard_rect, basket_rect, hoop_center_rect):
        if not self.active:
            return

            # Appliquer gravité et mouvement
        self.vel_y += gravity
        self.x += self.vel_x
        self.y += self.vel_y

        # Collision avec le sol
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

        # Collision avec les bords de l'écran
        if self.x - 10 <= 0 or self.x + 10 >= 1000:
            self.vel_x *= -0.6

        # Collision avec le panneau
        if self.rect().colliderect(backboard_rect):
            self.x -= self.vel_x  * 1.2
            self.y -= self.vel_y * 0.6
            self.vel_x *= -0.7


        # Collision avec l'anneau
        if self.rect().colliderect(basket_rect):
            if self.x < basket_rect.left + 5:
                self.x = basket_rect.left - 10
                self.vel_x *= -0.6
            elif self.x > basket_rect.right - 5:
                self.x = basket_rect.right + 10
                self.vel_x *= -0.6

        # Passage au centre du panier = score
        if self.rect().colliderect(hoop_center_rect):
            # Si la balle touche le panier par le bas => supprimer
            if self.vel_y < 0:
                self.active = False
                return
            if self.vel_y > 0 and not self.scored :
                self.scored = True
                self.active = False
                return "score"

        # Désactivation après repos
        if self.rest_time and time.time() - self.rest_time >= 1.5:
            self.active = False
        pass



    def draw(self, screen):
        screen.blit(self.ball_image, (int(self.x) - 10, int(self.y) - 10))

    def rect(self):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)