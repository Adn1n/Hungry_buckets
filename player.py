import pygame
from config import *
from ball import Ball
from arrow import Arrow
import math
import random


class Player :

    def __init__(self,screen):

        self.gravity = 0
        self.velocity = PLAYER_VELOCITY

        self.is_jumping = False
        self.jump_velocity = PLAYER_JUMP_VELOCITY



        self.spawn_1 = random.randint(560,910)
        self.spawn_2 = random.randint(70,470)
        self.spawn = random.choice([self.spawn_1,self.spawn_2])


        self.joueur = pygame.Rect(self.spawn, (SCREEN_HEIGHT - PLAYER_HEIGHT) - 90, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.sol_player = self.joueur.y

        self.joueur_arret = False

        self.arrow = Arrow(screen,self.spawn)
        print("spawn : ",self.spawn_1)


    def draw(self,ecran,font):
        pygame.draw.rect(ecran, PLAYER_COLOR, self.joueur)
        if self.joueur_arret:
            self.arrow.draw(ecran,font,self.joueur)



    def handle_event(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.is_jumping:
                    self.is_jumping = True
                    self.gravity = - self.jump_velocity
                if event.key == pygame.K_RETURN:
                    self.joueur_arret = not self.joueur_arret

        if self.joueur_arret:
            self.arrow.handle_events(self.joueur,self.spawn)
            return  # On quitte la méthode, donc aucune touche ne bouge le joueur


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.joueur.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.joueur.x += self.velocity

        if self.is_jumping:
            self.joueur.y += self.gravity
            self.gravity += 1
            if self.joueur.y >= self.sol_player:
                self.joueur.y = self.sol_player
                self.is_jumping = False
                self.gravity = 0

        if self.joueur.x < 0 :
            self.joueur.x = 0
        if self.joueur.x + self.joueur.w > SCREEN_WIDTH :
            self.joueur.x = SCREEN_WIDTH - self.joueur.w

        if 70 <= self.spawn <= 470:  # Si le joueur a spawné côté gauche
            self.joueur.x = max(70, min(self.joueur.x, 460))
        else:  # côté droit
            self.joueur.x = max(560, min(self.joueur.x, 850))



        if self.joueur.y < 0 :
            self.joueur.y = 0
        if  self.joueur.y > self.sol_player:
            self.joueur.y = self.sol_player




