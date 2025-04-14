import pygame
from player import Player
from config import *
from fonctions_utiles import *
from menu_screen import Menu

class Game :
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Projet Transverse")
        icone = pygame.image.load('image/icone.png')
        pygame.display.set_icon(icone)
        self.clock = pygame.time.Clock()

        self.reference_size = (1280, 720)

        self.player = Player()

        self.background_original = pygame.image.load("image/arriere_plan_basket.png")
        self.background = pygame.transform.scale(self.background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.font = pygame.font.SysFont('arial', FONT_SIZE)
        self.running = True



    def draw(self,ecran,font):

        self.ecran.fill((0,0,0))
        self.ecran.blit(self.background,(0,0))
        self.player.draw(self.ecran)
        self.pos = pygame.mouse.get_pos()

        afficher_texte(ecran,font,f"Gravity : {self.player.gravity}",(300,0),"orange")
        afficher_texte(ecran,font,f"Coordinates y : {self.player.joueur.y}",(0,0),"red")
        afficher_texte(ecran,font,f"Coordinates x : {self.player.joueur.x}",(0,20),"black")
        afficher_texte(ecran,font,f'position :{self.pos}',(600,0),'black')


        pygame.display.update()



    def handling(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.ecran = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                self.background = pygame.transform.scale(self.background_original, (event.w, event.h))

        self.player.handle_event(events)


    def run(self):
        while self.running:
            self.handling()
            self.draw(self.ecran,self.font)
            self.clock.tick(60)

        pygame.quit()



