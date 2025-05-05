import os
import pygame

from src.core.fenetre import Fenetre
from src.utils import *
from src.core.config import *

#
class ChoixJoueur():
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "choix_joueur.png")
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.SysFont("arial", 20)

        self.btn_rect_axel = pygame.Rect(560, 290, 230, 210)
        self.btn_rect_tyson = pygame.Rect(225, 285, 220, 215)


    def draw(self,screen):

        img_option = self.background
        screen.blit(img_option, (0, 0))

        btn_axel = self.btn_rect_axel
        btn_tyson = self.btn_rect_tyson

        pos = pygame.mouse.get_pos()
        afficher_texte(screen,self.font,f'pos : {pos[0]}, {pos[1]}',(0,0),'white')

        return btn_axel, btn_tyson