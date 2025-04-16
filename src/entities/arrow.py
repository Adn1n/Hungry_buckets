import pygame
import math
from src.utils.fonctions_utiles import afficher_texte


class Arrow:

    def __init__(self, screen, spawn):
        self.screen = screen
        self.angle = 90  # angle par défaut
        if spawn <= 500:
            # Si le joueur est à gauche, l’angle part de 45°
            self.angle = 45
        elif spawn >= 500:
            # Si le joueur est à droite, l’angle part de 135°
            self.angle = 135

        self.force = 45  # force initiale du tir
        self.ball = None  # instance de balle à tirer, initialement vide

    def draw(self, ecran, font, joueur):
        # Calcule la position de l'extrémité de la flèche en fonction de l'angle et de la force
        arrow_length = 10 + self.force
        rad = math.radians(self.angle)

        x_end = joueur.centerx + arrow_length * math.cos(rad)
        y_end = joueur.centery - arrow_length * math.sin(rad)

        # Trace le corps de la flèche
        pygame.draw.line(ecran, "blue", joueur.center, (x_end, y_end), 3)

        # Calcule et trace la tête de la flèche (deux lignes en biais)
        head_length = 10
        angle_offset = math.radians(20)

        x1 = x_end - head_length * math.cos(rad - angle_offset)
        y1 = y_end + head_length * math.sin(rad - angle_offset)

        x2 = x_end - head_length * math.cos(rad + angle_offset)
        y2 = y_end + head_length * math.sin(rad + angle_offset)

        pygame.draw.line(ecran, "black", (x_end, y_end), (x1, y1), 4)
        pygame.draw.line(ecran, "black", (x_end, y_end), (x2, y2), 4)

        # Affiche la force actuelle sur l’écran
        afficher_texte(ecran, font, f"Force : {self.force}", (300, 250), "black")

        # Si une balle est présente, on la met à jour et on la dessine
        if self.ball:
            print(">>> BALLE DESSINÉE")
            self.ball.update()
            self.ball.draw(ecran)

    def handle_events(self, joueur, spawn):
        keys = pygame.key.get_pressed()

        for key in keys:
            if 70 <= spawn <= 500:
                # Côté gauche : angle de 0 à 90
                if keys[pygame.K_RIGHT]:
                    self.angle = max(0, self.angle - 0.0025)
                if keys[pygame.K_LEFT]:
                    self.angle = min(90, self.angle + 0.0025)
            elif 510 <= spawn <= 910:
                # Côté droit : angle de 90 à 180
                if keys[pygame.K_RIGHT]:
                    self.angle = max(90, self.angle - 0.0025)
                if keys[pygame.K_LEFT]:
                    self.angle = min(180, self.angle + 0.0025)

            # Contrôle de la force du tir avec les flèches haut et bas
            if keys[pygame.K_UP]:
                self.force += 0.001
            if keys[pygame.K_DOWN]:
                self.force -= 0.001

        # Force minimale et maximale pour éviter les valeurs absurdes
        if self.force > 130:
            self.force = 130
        elif self.force < 15:
            self.force = 15
