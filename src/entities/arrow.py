import pygame
import math
import time

from pygame import K_RETURN

from src.utils.fonctions_utiles import afficher_texte
from src.entities.ball import Ball

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
        self.ball = None

        self.trajectoire_fixee = False
        self.verif_tir = False

        self.start_time = None
        self.initial_ball_pos = None


    def draw_arrow(self, ecran,player) :
        joueur = player.joueur
        arrow_length = 10 + self.force
        rad = math.radians(self.angle)

        x_end = joueur.centerx + arrow_length * math.cos(rad)
        y_end = joueur.centery - arrow_length * math.sin(rad)

        head_length = 10
        angle_offset = math.radians(20)

        x1 = x_end - head_length * math.cos(rad - angle_offset)
        y1 = y_end + head_length * math.sin(rad - angle_offset)

        x2 = x_end - head_length * math.cos(rad + angle_offset)
        y2 = y_end + head_length * math.sin(rad + angle_offset)

        pygame.draw.line(ecran, "blue", joueur.center, (x_end, y_end), 3)
        pygame.draw.line(ecran, "black", (x_end, y_end), (x1, y1), 4)
        pygame.draw.line(ecran, "black", (x_end, y_end), (x2, y2), 4)

        return x_end, y_end



    def draw(self, ecran, font, player):
        if not self.verif_tir:
            x_end, y_end = self.draw_arrow(ecran, player)
        else:
            # sinon, utilise la dernière position enregistrée
            x_end = self.ball.x
            y_end = self.ball.y


        if not self.ball:
            self.ball = Ball(x_end, y_end, self.angle, self.force, tir=False,sol=player.joueur.bottom)
            self.initial_ball_pos = (x_end, y_end)


        # Balle attachée à la flèche jusqu’à ce qu’on tire
        if not self.verif_tir:
            self.ball.x = x_end
            self.ball.y = y_end
        else:
            self.ball.tir = True  # elle commence à bouger
            if self.start_time is None:
                self.start_time = time.time()

        if self.start_time and time.time() - self.start_time > 3:
            x, y = self.initial_ball_pos
            self.ball = Ball(x, y, self.angle, self.force, tir=False, sol=player.joueur.bottom)
            player.respawn()
            # Recalculer la position de la flèche après le respawn
            joueur = player.joueur

            self.ball.x = x_end
            self.ball.y = y_end
            self.ball.tir = False


            self.verif_tir = False
            self.trajectoire_fixee = False
            self.start_time = None


        self.ball.update()
        self.ball.draw(ecran)





    def handle_events(self, joueur, spawn,events):
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.trajectoire_fixee:
                        self.trajectoire_fixee = True  # On fige la trajectoire
                if event.key == pygame.K_SPACE :
                    if self.trajectoire_fixee and not self.verif_tir:
                        self.verif_tir = True  # On lance le tir




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
