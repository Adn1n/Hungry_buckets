import os
import pygame
import math
import time

from src.core.config import *
#

class Ball:
    """
    Classe représentant une balle de basket.
    Gère la position, la vitesse, les collisions, le rendu et l'état de la balle.
    """

    def __init__(self, x, y, angle, power):
        """
        Initialise une balle avec une position, une vitesse initiale basée sur un angle et une puissance,
        et charge l'image associée.

        :param x: Position initiale en x
        :param y: Position initiale en y
        :param angle: Angle de tir en radians
        :param power: Puissance initiale du tir
        """
        # Position initiale de la balle
        self.x = x
        self.y = y

        # Vitesse initiale calculée à partir de l'angle et de la puissance
        self.vel_x = math.cos(angle) * power
        self.vel_y = math.sin(angle) * power

        # Indique si la balle est encore en mouvement ou active dans le jeu
        self.active = True

        # Temps auquel la balle s'est arrêtée (utilisé pour désactiver après un délai)
        self.rest_time = None

        # Indique si la balle a marqué un point
        self.scored = False

        # Construction du chemin vers l'image de la balle
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "Ball.png")

        # Chargement et redimensionnement de l'image de la balle
        self.ball_image = pygame.image.load(image_path)
        self.ball_image = pygame.transform.scale(self.ball_image, (50, 50))  # Ajuste la taille pour correspondre à la balle originale

        # Rayon de la balle, utilisé pour les calculs de collision
        self.ball_radius = self.ball_image.get_width() // 2



    def update(self, gravity, screen_height, backboard_rect, basket_rect, hoop_center_rect):
        """
        Met à jour la position et la vitesse de la balle en fonction de la gravité,
        gère les rebonds sur les bords de l'écran et les collisions avec les éléments du panier.
        Gère également les conditions de score et d'arrêt de la balle.

        :param gravity: Force de gravité appliquée à la balle
        :param screen_height: Hauteur de l'écran pour détecter le sol
        :param backboard_rect: Rect du panneau arrière pour collision
        :param basket_rect: Rect du panier pour collision
        :param hoop_center_rect: Rect du centre du cerceau pour collision et score
        :return: "score" si la balle marque un point, sinon None
        """
        if not self.active:
            # Si la balle n'est plus active, on ne fait pas de mise à jour
            return

        # Application de la gravité sur la vitesse verticale
        self.vel_y += gravity

        # Mise à jour des positions selon les vitesses
        self.x += self.vel_x
        self.y += self.vel_y

        # Gestion du rebond sur le sol (bas de l'écran)
        if self.y + self.ball_radius >= screen_height:
            self.y = screen_height - self.ball_radius  # Positionne la balle juste au sol
            if abs(self.vel_y) > 1:
                # Rebond amorti si la vitesse verticale est suffisante
                self.vel_y *= -0.5
                self.vel_x *= 0.95  # Perte légère de vitesse horizontale
            else:
                # Si la vitesse verticale est faible, la balle s'arrête
                self.vel_y = 0
                self.vel_x = 0
                if self.rest_time is None:
                    # Enregistre le temps d'arrêt pour désactivation ultérieure
                    self.rest_time = time.time()

        # Rebond sur le côté gauche de l'écran
        if self.x - self.ball_radius <= 0:
            self.x = self.ball_radius  # Positionne la balle au bord gauche
            self.vel_x *= -0.8  # Rebond plus doux sur l'axe horizontal
            self.vel_y *= 0.95  # Légère perte d’énergie verticale

        # Rebond sur le côté droit de l'écran
        elif self.x + self.ball_radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.ball_radius  # Positionne la balle au bord droit
            self.vel_x *= -0.8  # Rebond plus doux sur l'axe horizontal
            self.vel_y *= 0.95  # Légère perte d’énergie verticale

        # Collision avec les bords extrêmes de l'écran (zones proches des limites)
        if self.x - 10 <= 0 or self.x + 10 >= 1000:
            self.vel_x *= -0.6  # Rebond plus amorti horizontalement

        # Collision avec le panneau arrière du panier
        if self.rect().colliderect(backboard_rect):
            self.x -= self.vel_x  # Recule la balle pour éviter chevauchement
            self.vel_x *= -0.7  # Rebond amorti sur l'axe horizontal

        # Collision avec le panier (anneau)
        if self.rect().colliderect(basket_rect):
            self.x -= self.vel_x  # Recule la balle pour éviter chevauchement
            self.vel_x *= -0.6  # Rebond amorti sur l'axe horizontal

        # Détection de score : collision avec le centre du cerceau en descente et pas encore marqué
        if self.rect().colliderect(hoop_center_rect) and self.vel_y > 0 and not self.scored:
            self.active = False  # Désactive la balle car elle a marqué
            self.scored = True
            return "score"

        # Si la balle touche le fond du cerceau venant d'en dessous, on la désactive sans marquer
        if self.rect().colliderect(hoop_center_rect) and self.vel_y < 0:
            self.active = False
            return

        # Désactivation de la balle après un certain temps d'arrêt sur le sol
        if self.rest_time and time.time() - self.rest_time > 1.5:
            self.active = False



    def draw(self, screen):
        """
        Dessine la balle à l'écran en positionnant l'image centrée sur la position (x, y).

        :param screen: Surface Pygame sur laquelle dessiner la balle
        """
        # Place l'image de la balle en ajustant pour que le centre corresponde à (self.x, self.y)
        screen.blit(self.ball_image, (int(self.x - self.ball_radius), int(self.y - self.ball_radius)))



    def rect(self):
        """
        Retourne un rectangle pygame correspondant à la zone occupée par la balle,
        utilisé pour les détections de collision.

        :return: pygame.Rect représentant la zone de la balle
        """
        return pygame.Rect(self.x - self.ball_radius, self.y - self.ball_radius, self.ball_radius * 2, self.ball_radius * 2)