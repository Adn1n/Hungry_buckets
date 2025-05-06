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

        return jouer_rect, options_rect, quitter_rect

    def draw_game_over(self, screen, width, height, score, high_scores):
        screen.fill((255, 255, 255))
        msg = self.big_font.render("Fin de la partie", True, (0, 0, 0))
        screen.blit(msg, msg.get_rect(center=(width // 2, height // 2 - 120)))

        score_msg = self.font.render(f"Score : {score}", True, (0, 0, 0))
        screen.blit(score_msg, score_msg.get_rect(center=(width // 2, height // 2 - 60)))

        label = self.font.render("Meilleurs scores :", True, (0, 0, 0))
        screen.blit(label, label.get_rect(center=(width // 2, height // 2)))

        high_scores_sorted = sorted(high_scores, reverse=True)[:3]
        y_offset = 40
        for i in range(3):
            if i < len(high_scores_sorted):
                text = f"{i+1}. {high_scores_sorted[i]}"
            else:
                text = f"{i+1}. -"
            score_line = self.font.render(text, True, (0, 0, 0))
            screen.blit(score_line, (width // 2 - 50, height // 2 + y_offset))
            y_offset += 40

        replay_btn = pygame.Rect(width - 160, height - 80, 140, 50)
        pygame.draw.rect(screen, (200, 200, 200), replay_btn)
        pygame.draw.rect(screen, (0, 0, 0), replay_btn, 2)
        text = self.font.render("Rejouer", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=replay_btn.center))

        return replay_btn