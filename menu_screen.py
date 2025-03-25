import pygame
from config import *
from fonctions_utiles import *


class Menu :

    def __init__(self, ecran):
        self.menu_img = pygame.image.load("image/menu_basket.png")
        self.menu_img = pygame.transform.scale(self.menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ecran = ecran
        self.font = pygame.font.SysFont('arial', FONT_SIZE)
        self.bouton_nouvelle_partie = pygame.Rect(370,207,258,51)


    def handle(self):
        in_menu = True
        while in_menu:
            events = pygame.event.get()
            action = self.draw(self.ecran,self.font,events)
            if action == "jouer":
                in_menu = False
                return True

            for event in events:
                if event.type == pygame.QUIT:
                    in_menu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_menu = False
                    if event.key == pygame.K_RETURN:
                        in_menu = False



    def draw(self,ecran,font,events):

            self.clock = pygame.time.Clock()
            self.ecran.blit(self.menu_img, (0, 0))  # fond noir

            pos = pygame.mouse.get_pos()

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Clic détecté à :", event.pos)
                    if self.bouton_nouvelle_partie.collidepoint(event.pos):
                        click = event.pos
                        return "jouer"

            afficher_texte(ecran,font,f"{pos}", (10, 10), "white")

            pygame.display.update()
            self.clock.tick(60)

