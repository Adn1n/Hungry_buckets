from src.core.config import *
from src.entities.arrow import Arrow
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


    def respawn(self):
        self.spawn = random.choice([self.spawn_1, self.spawn_2])
        self.joueur.x = self.spawn
        self.joueur.y = self.sol_player


    def draw(self,ecran,font):
        pygame.draw.rect(ecran, PLAYER_COLOR, self.joueur)
        if self.joueur_arret:
            self.arrow.draw(ecran,font,self)


    def handle_event(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not self.is_jumping:
                    # Déclenche un saut si le joueur n'est pas déjà en train de sauter
                    self.is_jumping = True
                    self.gravity = - self.jump_velocity
                if event.key == pygame.K_RETURN:
                    # Active ou désactive l'état d'arrêt du joueur
                    self.joueur_arret = not self.joueur_arret

        if self.joueur_arret:
            # Si le joueur est à l'arrêt, permet de contrôler la flèche et bloque les mouvements du joueur
            self.arrow.handle_events(self.joueur,self.spawn,events)
            return  # On quitte la méthode, donc aucune touche ne bouge le joueur

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Déplace le joueur vers la gauche
            self.joueur.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            # Déplace le joueur vers la droite
            self.joueur.x += self.velocity

        if self.is_jumping:
            # Applique la gravité pour simuler un saut
            self.joueur.y += self.gravity
            self.gravity += 1
            if self.joueur.y >= self.sol_player:
                # Le joueur atterrit
                self.joueur.y = self.sol_player
                self.is_jumping = False
                self.gravity = 0

        # Empêche le joueur de sortir de l'écran horizontalement
        if self.joueur.x < 0 :
            self.joueur.x = 0
        if self.joueur.x + self.joueur.w > SCREEN_WIDTH :
            self.joueur.x = SCREEN_WIDTH - self.joueur.w

        # Contraint le joueur à rester dans sa zone de spawn (gauche ou droite)
        if 70 <= self.spawn <= 470:
            self.joueur.x = max(70, min(self.joueur.x, 460))
        else:
            self.joueur.x = max(560, min(self.joueur.x, 850))

        # Empêche le joueur de sortir verticalement de l'écran
        if self.joueur.y < 0 :
            self.joueur.y = 0
        if  self.joueur.y > self.sol_player:
            self.joueur.y = self.sol_player

