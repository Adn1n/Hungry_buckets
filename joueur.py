import pygame
from config import *


class Player :

    def __init__(self):

        self.gravity = 0
        self.velocity = PLAYER_VELOCITY

        self.is_jumping = False
        self.jump_velocity = PLAYER_JUMP_VELOCITY

        self.joueur = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2, (SCREEN_HEIGHT - PLAYER_HEIGHT) - 90, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.sol_player = self.joueur.y


    def draw(self, ecran):
        pygame.draw.rect(ecran, PLAYER_COLOR, self.joueur)


    def handle_event(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.is_jumping:
                    self.is_jumping = True
                    self.gravity = - self.jump_velocity

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

        if self.joueur.y < 0 :
            self.joueur.y = 0
        if  self.joueur.y > self.sol_player:
            self.joueur.y = self.sol_player



