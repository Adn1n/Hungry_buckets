import pygame
from joueur import Player
from config import *

class Game :
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Projet Transverse")
        icone = pygame.image.load('image/icone.png')
        pygame.display.set_icon(icone)
        self.clock = pygame.time.Clock()

        self.player = Player(self.ecran.get_width(),self.ecran.get_height())

        print(self.ecran.get_width(),self.ecran.get_height())
        self.font = pygame.font.SysFont(None, 40)

        self.running = True


    def afficher_texte(self,texte,position,couleur):
        rendu = self.font.render(texte, True, couleur)
        self.ecran.blit(rendu,position)


    def draw(self):

        self.ecran.fill('white')
        self.player.draw(self.ecran)

        self.afficher_texte(f"Gravity : {self.player.gravity}",(300,0),"orange")
        self.afficher_texte(f"Coordinates : {self.player.joueur.y}",(0,0),"red")

        pygame.display.update()

    def handling(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.player.handle_event(events)


    def run(self):
        while self.running:
            self.handling()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

pygame.init()
game = Game()
game.run()

