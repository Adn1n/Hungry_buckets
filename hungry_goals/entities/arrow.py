import pygame
import math

from hungry_goals.engine.config import *

# Classe Arrow : gère la simulation et l'affichage de la trajectoire d'une flèche (ou balle)
# en tenant compte de la gravité et des rebonds sur les bords de la fenêtre.
class Arrow:
    def __init__(self, gravity=0.5, color=(0, 0, 0)):
        """
        Constructeur de la classe Arrow.
        :param gravity: Accélération due à la gravité appliquée à chaque étape (float).
        :param color: Couleur principale de la flèche (tuple RGB), utilisée pour d'autres dessins éventuels.
        Attributs :
            self.gravity : gravité appliquée à la trajectoire.
            self.color : couleur de la flèche.
        """
        self.gravity = gravity
        self.color = color

    def draw_trajectory(self, surface, start_pos, angle, power, steps=50):
        """
        Dessine la trajectoire prédite de la flèche en tenant compte de la gravité et des rebonds.
        :param surface: Surface pygame sur laquelle dessiner.
        :param start_pos: Tuple (x, y) indiquant la position initiale de la flèche.
        :param angle: Angle de tir en radians.
        :param power: Puissance du tir (vitesse initiale).
        :param steps: Nombre d'étapes de simulation pour la trajectoire.
        """
        # Initialisation de la position de départ (convertie en float pour la précision)
        x = float(start_pos[0])
        y = float(start_pos[1])
        # Calcul des composantes de la vitesse initiale selon l'angle et la puissance
        vel_x = math.cos(angle) * power
        vel_y = math.sin(angle) * power
        # Rayon de la balle (importé depuis la config)
        radius = BALL_RADIUS  # doit être importé depuis config

        for i in range(steps):
            # Temps simulé (le pas peut être ajusté pour raffiner l'affichage)
            t = i * 0.5  # par exemple 0.5 secondes entre chaque point

            # Formules explicites basées sur les équations du mouvement parabolique
            x = start_pos[0] + math.cos(angle) * power * t
            y = start_pos[1] + math.sin(angle) * power * t + 0.5 * self.gravity * t ** 2

            # Vérifie si la position est encore dans la fenêtre, sinon on arrête la simulation
            if 0 <= x <= surface.get_width() and 0 <= y <= surface.get_height():
                # Dessine un cercle pour représenter la position de la flèche à cette étape
                pygame.draw.circle(surface, (200, 0, 200), (int(x), int(y)), 4)
            else:
                break

            # Application de la gravité à la vitesse verticale
            vel_y += self.gravity

            # Gestion du rebond contre le sol (bord inférieur)
            if y + radius >= surface.get_height():
                # Replace la balle juste au-dessus du sol pour éviter de passer au travers
                y = surface.get_height() - radius
                # Si la vitesse verticale est suffisante, rebondit avec perte d'énergie
                if abs(vel_y) > 1:
                    vel_y *= -0.5   # Inverse et réduit la vitesse verticale (rebond amorti)
                    vel_x *= 0.95   # Amortit aussi la vitesse horizontale pour simuler le frottement
                else:
                    # Si la vitesse est trop faible, on arrête la simulation (la balle "s'arrête")
                    break

            # Gestion du rebond contre le mur gauche
            if x - radius <= 0:
                x = radius  # Replace la balle juste à l'intérieur du mur
                vel_x *= -0.8  # Inverse et réduit la vitesse horizontale (rebond amorti)
            # Gestion du rebond contre le mur droit
            elif x + radius >= surface.get_width():
                x = surface.get_width() - radius
                vel_x *= -0.8