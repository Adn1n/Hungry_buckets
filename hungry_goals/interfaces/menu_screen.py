# Projet : Hungry Buckets
# Description : Gère les écrans de menu principal et d'écran de fin avec leurs boutons et affichages de score.

import os
import pygame
from pygame import mouse

from hungry_goals.engine.config import *
from hungry_goals.utils import *
from hungry_goals.engine.score_manager import *
#
class MenuScreen:
    def __init__(self):
        self.score_manager = ScoreManager()
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
        """
        Affiche l'écran de démarrage avec fond et boutons, et retourne leurs zones cliquables.

        Paramètres:
            screen (pygame.Surface): La surface sur laquelle dessiner.
            width (int): Largeur de l'écran.
            height (int): Hauteur de l'écran.

        Retour:
            tuple: Rectangles des zones cliquables pour jouer, options et quitter.
        """
        # Afficher le fond
        bg = self.menu_bg.copy()
        screen.blit(bg, (0, 0))

        # Créer les zones de boutons
        jouer_rect = self.btn_jouer
        options_rect = self.btn_options
        quitter_rect = self.btn_quitter


        # ➕ Zone du record
        record_rect = pygame.Rect(405, 448, 167, 42)

        # Gérer l’affichage du record s’il existe
        if os.path.exists("high_scores.txt"):
            with open("high_scores.txt", "r") as f:
                scores = [int(line.strip()) for line in f if line.strip().isdigit()]
                if scores:
                    best_score = max(scores)
                    text_surface = self.font.render(f"Record : {best_score}", True, (0, 255, 255))
                    text_rect = text_surface.get_rect(center=record_rect.center)
                    screen.blit(text_surface, text_rect)

        return jouer_rect, options_rect, quitter_rect

    def draw_game_over(self, screen, width, height, score, high_score):
        # --- Détection si un nouveau record est atteint ---
        is_record = score > high_score

        bg_path = None

        # --- Sauvegarde du score si record ---
        if is_record:
            self.score_manager.save_high_score(score)

        # --- Choix du fond selon le score ---
        if score < 10:
            bg_path = os.path.join("assets", "image", "game_over.png")
        elif score >= 10:
            bg_path = os.path.join("assets", "image", "game_win.png")

        # --- Affichage du fond si disponible ---
        if bg_path and os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (width, height))
            screen.blit(bg, (0, 0))

        # --- Affichage des boutons et du score (selon succès ou échec) ---
        if score >= 10:
            btn_menu = pygame.Rect(380, 330, 240, 55)
            btn_rejouer = pygame.Rect(380, 430, 240, 50)
            text = self.big_font.render(f"Score : {score}", True, TEXT_COLOR)
            screen.blit(text, text.get_rect(center=(width // 2, 250)))  # ajuste la hauteur si besoin
            return btn_menu, btn_rejouer
        else:
            btn_menu = pygame.Rect(330, 280, 340, 65)
            btn_rejouer = pygame.Rect(330, 370, 340, 65)
            score_text = self.big_font.render(f"Score : {score}", True, TEXT_COLOR)
            screen.blit(score_text, score_text.get_rect(center=(width // 2, 250)))
            return btn_menu, btn_rejouer




