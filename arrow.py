import pygame
import math
from ball import Ball
from fonctions_utiles import afficher_texte


class Arrow:

    def __init__(self, screen,spawn,spawn_1,spawn_2):
        self.screen = screen
        if spawn >= spawn_1:
            self.angle = 135  # angle de tir initial en degrés
        elif spawn >= spawn_2:
            self.angle = 45


        self.force = 75  # force du tir
        self.ball = None  # balle tirée

    def draw(self,ecran,font,joueur):
        arrow_length = 10 + self.force
        rad = math.radians(self.angle)

        x_end = joueur.centerx + arrow_length * math.cos(rad)
        y_end = joueur.centery - arrow_length * math.sin(rad)

        pygame.draw.line(ecran, "blue", joueur.center, (x_end, y_end), 3)

        head_length = 10
        angle_offset = math.radians(20)

        x1 = x_end - head_length * math.cos(rad - angle_offset)
        y1 = y_end + head_length * math.sin(rad - angle_offset)

        x2 = x_end - head_length * math.cos(rad + angle_offset)
        y2 = y_end + head_length * math.sin(rad + angle_offset)

        pygame.draw.line(ecran, "black", (x_end, y_end), (x1, y1), 4)
        pygame.draw.line(ecran, "black", (x_end, y_end), (x2, y2), 4)

        afficher_texte(ecran,font,f"Force : {self.force}",(300,250),"black")

    def handle_events(self,joueur):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_RIGHT]:
                self.angle =  max(0,self.angle - 0.0025)
            if keys[pygame.K_LEFT]:
                self.angle = min(180,self.angle + 0.0025)
            if keys[pygame.K_UP]:
                self.force += 0.001
            if keys[pygame.K_DOWN]:
                self.force -= 0.001

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.ball:
                    self.ball = Ball(joueur.centerx, joueur.centery, self.angle, self.force)

        if self.force > 130 :
            self.force = 130
        elif self.force < 15:
            self.force = 15




