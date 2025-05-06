import os
import pygame
from pygame import mouse

from src.core.config import *
from src.core.game import *
from src.utils import afficher_texte

####
class OptionScreen:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "option_screen.png")
        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.SysFont("arial", 20)

        # Rects cliquables (invisibles)
        self.sound_btn = pygame.Rect(350, 260, 275, 70)
        self.music_btn = pygame.Rect(350, 360, 275, 65)
        self.back_btn = pygame.Rect(340, 460, 280, 50)  # ajuste selon la vraie position du bouton << BACK

    def draw(self,screen):

        img_option = self.background
        screen.blit(img_option, (0, 0))

        sound_btn_rect = self.sound_btn
        music_btn_rect = self.music_btn
        back_btn_rect = self.back_btn

        pos = mouse.get_pos()
        afficher_texte(screen,self.font,f'pos : {pos[0]}, {pos[1]}',(0,0),'white')

        return sound_btn_rect, music_btn_rect, back_btn_rect
