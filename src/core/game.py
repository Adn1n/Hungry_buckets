import pygame
import os
import math
import time
import random

from src.core.config import *
from src.core.fenetre import Fenetre
from src.entities.player import Player
from src.entities.ball import Ball
from src.entities.panier import Panier
from src.entities.arrow import Arrow
from src.ui.menu_screen import MenuScreen
from src.ui.ecran import Ecran
from src.ui.option_screen import OptionScreen


class Game:
    def __init__(self):
        pygame.init()

        self.window = Fenetre("Hungry Goals")
        self.screen = self.window.get_screen()


        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        icon_path = os.path.join(base_path, "assets", "image", "logo.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        self.ecran = Ecran(self.screen)
        self.ecran.show_loading_screen()

        self.clock = pygame.time.Clock()

        # Objets du jeu
        self.player = Player(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
        self.arrow = Arrow()
        self.panier = Panier()
        self.menu = MenuScreen()
        self.option_screen = OptionScreen()

        # État du jeu
        self.ball_list = []
        self.score = 0
        self.high_scores = []
        self.dragging = False
        self.start_pos = None
        self.game_started = False
        self.game_over = False
        self.start_time = None

        self.option = False
        self.choix_joueur = False


        pygame.display.flip()


    def run(self):
        running = True
        while running:

            if self.option:
                sound_btn_rect, music_btn_rect, back_btn_rect = self.option_screen.draw(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if sound_btn_rect.collidepoint(event.pos):
                            print("Sound button clicked")
                        elif music_btn_rect.collidepoint(event.pos):
                            print("Music button clicked")
                        elif back_btn_rect.collidepoint(event.pos):
                            self.option = False
                self.clock.tick(60)
                continue

            if not self.game_started:
                jouer_btn, options_btn, quitter_btn = self.menu.draw_start_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if jouer_btn.collidepoint(event.pos):
                            self.start_time = time.time()
                            self.game_started = True
                            self.game_over = False
                            self.player = Player(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                        elif options_btn.collidepoint(event.pos):
                            self.option = True
                        elif quitter_btn.collidepoint(event.pos):
                            pygame.quit()
                            exit()



            if self.game_over:
                btn = self.menu.draw_game_over(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.score, self.high_scores)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos):
                        self.high_scores.append(self.score)
                        self.reset_game()
                self.clock.tick(60)
                continue


            # Gameplay
            if not self.start_time:
                continue

            elapsed = time.time() - self.start_time
            remaining = max(0, int(60 - elapsed))
            if remaining <= 0:
                self.high_scores.append(self.score)
                self.game_over = True
                continue

            self.screen.fill(WHITE)

            # Chrono
            self.screen.blit(self.menu.font.render(f"Time: {remaining}", True, BLACK), (20, 20))
            if remaining <= 3:
                txt = self.menu.huge_font.render(str(remaining), True, BLACK)
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            # Input
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, SCREEN_WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_pos = pygame.mouse.get_pos()
                    self.dragging = True
                    self.player.start_shoot()

                elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
                    end_pos = pygame.mouse.get_pos()
                    self.player.state = "idle"
                    self.player.frames = self.player.frames_idle
                    self.player.frame_index = 0

                    if self.start_pos and self.start_pos != end_pos:
                        player_pos = self.player.get_position()

                        dx = self.start_pos[0] - end_pos[0]
                        dy = self.start_pos[1] - end_pos[1]
                        angle = math.atan2(dy, dx)
                        power = min(math.hypot(dx, dy) / 4, 20)

                        self.ball_list.append(Ball(player_pos[0], player_pos[1], angle, power))

                    self.dragging = False
                    self.start_pos = None


            # Affichage
            self.player.draw(self.screen)
            self.panier.draw(self.screen)

            # ➕ Flèche de visée quand on vise
            # ➕ Flèche de visée quand on vise
            if self.dragging and self.start_pos:
                current_mouse_pos = pygame.mouse.get_pos()
                player_pos = self.player.get_position()
                self.arrow.draw(self.screen, player_pos, self.start_pos, current_mouse_pos)


            backboard_rect, basket_rect, hoop_center_rect = self.panier.get_rects()

            for ball in self.ball_list:
                if ball.active:
                    result = ball.update(GRAVITY, SCREEN_HEIGHT, backboard_rect, basket_rect, hoop_center_rect)
                    if result == "score":
                        self.score += 1
                        self.player = Player(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                        new_y = random.randint(200, SCREEN_HEIGHT - 250)  # évite le haut et le bas
                        self.panier.basket_rect.y = new_y
                        self.panier.backboard_rect.y = new_y - 50  # ajuste selon ta hauteur
                        self.panier.hoop_center_rect.y = self.panier.basket_rect.bottom
                    ball.draw(self.screen)

            self.ball_list = [b for b in self.ball_list if b.active]

            # Score & record
            self.screen.blit(self.menu.font.render(f"Score: {self.score}", True, BLACK), (SCREEN_WIDTH - 200, 40))
            record = max(self.high_scores) if self.high_scores else "-"
            self.screen.blit(self.menu.font.render(f"Record: {record}", True, BLACK), (SCREEN_WIDTH - 200, 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def reset_game(self):
        self.ball_list = []
        self.score = 0
        self.start_time = time.time()
        self.dragging = False
        self.start_pos = None
        self.game_started = True
        self.game_over = False
        self.player = Player(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)


if __name__ == "__main__":
    game = Game()
    game.run()
