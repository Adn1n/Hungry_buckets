import os
import pygame
from pygame import mouse

from src.core.config import *
from src.utils import *
#
class MenuScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)
        self.huge_font = pygame.font.SysFont(None, 120)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "menu.png")
        self.menu_bg = pygame.image.load(image_path)
        self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.btn_jouer = pygame.Rect(330, 220, 305, 65)
        self.btn_options = pygame.Rect(345, 305, 280, 50)
        self.btn_quitter = pygame.Rect(370, 380, 230, 45)

    def draw_start_screen(self, screen, width, height):
        bg = self.menu_bg.copy()
        screen.blit(bg, (0, 0))

        jouer_rect = self.btn_jouer
        options_rect = self.btn_options
        quitter_rect = self.btn_quitter

        pos = mouse.get_pos()
        afficher_texte(screen,self.font,f'Pos : {pos[0]}, {pos[1]}',(0,0),'white')

        # ➕ Zone du record
        record_rect = pygame.Rect(405, 448, 167, 42)

        if os.path.exists("high_scores.txt"):
            with open("high_scores.txt", "r") as f:
                scores = [int(line.strip()) for line in f if line.strip().isdigit()]
                if scores:
                    best_score = max(scores)
                    text_surface = self.font.render(f"Record : {best_score}", True, (0, 255, 255))
                    text_rect = text_surface.get_rect(center=record_rect.center)
                    screen.blit(text_surface, text_rect)

        return jouer_rect, options_rect, quitter_rect

    def draw_game_over(self, screen, width, height, score,high_score):
        # Lire le record existant depuis le fichier

        is_record = score > high_score

        bg_path = None

        # Enregistre le nouveau record si battu
        if is_record:
            save_high_score(score)

        # Choisir le fond en fonction du résultat
        if score < 10:
            bg_path = os.path.join("assets", "image", "game_over.png")
        elif score >= 10:
            bg_path = os.path.join("assets", "image", "game_win.png")

        # Affichage du fond
        if bg_path and os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (width, height))
            screen.blit(bg, (0, 0))

        pos = mouse.get_pos()
        afficher_texte(screen,self.font,f'pos : {pos}',(0,0),'white')

        if score >= 10 :
            btn_menu = pygame.Rect(380, 330, 240, 55)
            btn_rejouer = pygame.Rect(380, 430, 240, 50)
            return btn_menu, btn_rejouer
        else:
            btn_menu = pygame.Rect(330, 280, 340, 65)
            btn_rejouer = pygame.Rect(330, 370, 340, 65)
            return btn_menu, btn_rejouer




