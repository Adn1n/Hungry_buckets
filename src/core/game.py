import pygame
import os
import math
import time
import random


from src.core.config import *
from src.utils import *
from src.core.fenetre import Fenetre
from src.entities.player1 import*
from src.entities.player2 import*
from src.entities.ball import Ball
from src.entities.panier import Panier
from src.entities.arrow import Arrow
from src.ui.menu_screen import MenuScreen
from src.core.backgroung import BackgroundManager
from src.ui.ecran import Ecran
from src.ui.option_screen import OptionScreen
from src.ui.choix_joueur import ChoixJoueur
from src.core.music_manager import MusicManager
from src.core.score_manager import ScoreManager
from src.entities.bonus_item import BonusItem

#
class Game:
    def __init__(self):
        pygame.init()

        self.window = Fenetre("Hungry Goals")
        self.screen = self.window.get_screen()
        self.font = pygame.font.SysFont("comicsans", 30)


        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        icon_path = os.path.join(base_path, "assets", "image", "logo.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        background_path = os.path.join(base_path, "assets", "image", "background.png")
        self.background = BackgroundManager(background_path, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ecran = Ecran(self.screen)
        self.ecran.show_loading_screen()

        self.start_time = time.time()  # 🟢 On revient à l’ancien système
        self.clock = pygame.time.Clock()

        self.player = None


        # Objets du jeu
        self.player1 = Player1(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
        self.player2 = Player2(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
        self.arrow = Arrow()
        self.panier = Panier()
        self.menu = MenuScreen()
        self.option_screen = OptionScreen()
        self.choix_joueur = ChoixJoueur()

        self.bonus_items = []
        self.last_bonus_spawn = time.time()

        # État du jeu
        self.ball_list = []
        self.score = 0
        self.dragging = False
        self.start_pos = None
        self.game_started = False
        self.game_over = False
        self.start_time = None

        self.is_new_record = False

        self.option = False
        self.afficher_choix_joueur = False

        self.preview_angle = None
        self.preview_power = None

        self.challenge_mode = False
        self.final_screen_shown = False
        self.final_screen_start = None
        self.challenge_timer = 0
        self.challenge_timer = time.time()

        self.total_score = 0  # Score classique + challenge
        pygame.display.flip()

        self.score_manager = ScoreManager()
        self.high_score = self.score_manager.load_high_score()

        music_path = os.path.join("assets", "sounds", "musique.mp3")
        self.music = MusicManager(music_path)
        self.music.play()


    def run(self):
        running = True

        while running:

            if self.final_screen_shown:
                if time.time() - self.final_screen_start < 2:

                    image_path = os.path.join("assets", "image", "niveau_finale.png")
                    challenge_img = pygame.image.load(image_path)
                    challenge_img = pygame.transform.scale(challenge_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # adapte la taille si besoin
                    self.screen.blit(challenge_img, challenge_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

                    pygame.display.flip()
                    self.clock.tick(60)
                    continue
                else:
                    self.final_screen_shown = False
                    self.challenge_mode = True
                    self.start_time = time.time()
                    self.total_score = self.score
                    self.score = 0
                    self.score_challenge = 0
                    self.ball_list.clear()
                    self.panier.repositionner()
                    continue

            if self.option:
                sound_btn_rect, music_btn_rect, back_btn_rect = self.option_screen.draw(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if sound_btn_rect.collidepoint(event.pos):
                            print("Sound button clicked")
                        elif music_btn_rect.collidepoint(event.pos):
                            if pygame.mixer.music.get_busy():
                                self.music.pause()
                            else:
                                self.music.resume()
                        elif back_btn_rect.collidepoint(event.pos):
                            self.option = False
                self.clock.tick(60)
                continue

            if self.afficher_choix_joueur:
                axel_rect, tyson_rect, retour_rect = self.choix_joueur.draw(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if axel_rect.collidepoint(event.pos):
                            self.start_time = time.time()
                            self.game_started = True
                            self.afficher_choix_joueur = False  # ✅ ajoute ça !
                            self.player2 = Player2(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                            self.player = self.player2
                        elif tyson_rect.collidepoint(event.pos):
                            self.start_time = time.time()
                            self.game_started = True
                            self.afficher_choix_joueur = False  # ✅ ajoute ça !
                            self.player1 = Player1(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                            self.player = self.player1
                        elif retour_rect.collidepoint(event.pos):
                            self.start_time = None
                            self.afficher_choix_joueur = False
                            self.game_started = False
                            self.player = None  # évite le crash si aucun joueur sélectionné
                continue  # ✅ empêche le menu de s'afficher par-dessus

            if not self.game_started:
                jouer_btn, options_btn, quitter_btn = self.menu.draw_start_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if jouer_btn.collidepoint(event.pos):
                            self.afficher_choix_joueur = True
                        elif options_btn.collidepoint(event.pos):
                            self.option = True
                        elif quitter_btn.collidepoint(event.pos):
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            pygame.quit()
                            exit()







            if self.game_over:
                btn_menu, btn_rejouer = self.menu.draw_game_over(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.total_score + self.score,self.high_score)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.is_new_record = True
                            self.high_score = total
                            high_score = self.score
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total

                        if btn_menu.collidepoint(event.pos):
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            self.start_time = None
                            self.game_over = False
                            self.game_started = False
                            self.player = None
                        elif btn_rejouer.collidepoint(event.pos):
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            self.reset_game()

                self.clock.tick(60)
                continue


            # Gameplay
            if not self.start_time:
                continue

            elapsed = time.time() - self.start_time
            remaining = max(0, int(TEMPS_JEU - elapsed))

            if remaining <= 0:
                total = self.total_score + self.score
                if total > self.high_score:
                    self.score_manager.save_high_score(total)
                    self.high_score = total
                    self.is_new_record = True  # si tu veux afficher "Nouveau record"


                if self.score >= 12 and not self.challenge_mode:
                    self.final_screen_shown = True
                    self.final_screen_start = time.time()
                    continue

                self.game_over = True
                continue

            self.background.draw(self.screen)

            # Chrono
            chrono_text = self.menu.font.render(f"Time: {remaining}", True, TEXT_COLOR)
            self.screen.blit(chrono_text, chrono_text.get_rect(center=(SCREEN_WIDTH // 2, 20)))

            if remaining <= 3:
                txt = self.menu.huge_font.render(str(remaining), True, (255, 0, 255))  # Rose néon
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            # Input
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, SCREEN_WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    total = self.total_score + self.score
                    if total > self.high_score:
                        self.score_manager.save_high_score(total)
                        self.high_score = total
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_pos = pygame.mouse.get_pos()
                    self.dragging = True
                    self.player.start_shoot()

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    current_mouse = pygame.mouse.get_pos()
                    dx = self.start_pos[0] - current_mouse[0]
                    dy = self.start_pos[1] - current_mouse[1]
                    self.preview_angle = math.atan2(dy, dx)
                    self.preview_power = min(math.hypot(dx, dy) / 5, 24)


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
                        power = min(math.hypot(dx, dy) / 5, 24)

                        self.ball_list.append(Ball(player_pos[0], player_pos[1], angle, power))

                    self.dragging = False
                    self.start_pos = None
                    self.preview_angle = None
                    self.preview_power = None


            # Affichage
            self.player.draw(self.screen)
            self.panier.draw(self.screen)

            # ➕ Flèche de visée quand on vise
            # ➕ Flèche de visée quand on vise
            if self.dragging and self.start_pos:
                current_mouse_pos = pygame.mouse.get_pos()
                player_pos = self.player.get_position()
                if self.preview_angle is not None and self.preview_power is not None:
                    self.arrow.draw_trajectory(self.screen, player_pos, self.preview_angle, self.preview_power)


            backboard_rect, basket_rect, hoop_center_rect = self.panier.get_rects()

            for ball in self.ball_list:
                if ball.active:
                    result = ball.update(GRAVITY, SCREEN_HEIGHT, backboard_rect, basket_rect, hoop_center_rect)
                    if result == "score":
                        self.score += POINT_SCORE
                        self.panier.repositionner()
                        player_x = random.randint(100, 750)
                        if self.challenge_mode:
                            self.player.x = random.randint(100, 750)  # reposition rapide du joueur
                    ball.draw(self.screen)

            self.ball_list = [b for b in self.ball_list if b.active]

            if self.challenge_mode:
                if time.time() - self.challenge_timer > 2:
                    self.panier.repositionner()
                    self.challenge_timer = time.time()
                # ➕ Spawn bonus toutes les 5 secondes
                if time.time() - self.last_bonus_spawn > 5:
                    bonus = BonusItem("assets/image/bonus.png", SCREEN_WIDTH)
                    self.bonus_items.append(bonus)
                    self.last_bonus_spawn = time.time()

            for bonus in self.bonus_items:
                bonus.update()
                bonus.draw(self.screen)

                # Collision avec le joueur
                if self.player.rect.colliderect(bonus.rect):
                    self.start_time += 5
                    self.bonus_items.remove(bonus)

            # Supprimer ceux qui sortent de l’écran
            self.bonus_items = [b for b in self.bonus_items if not b.is_off_screen(SCREEN_HEIGHT)]

            # Score & record
            self.screen.blit(self.menu.font.render(f"Score: {self.score}", True, TEXT_COLOR), (20, 20))
            record = self.score_manager.load_high_score()
            self.screen.blit(self.menu.font.render(f"Record: {record}", True, TEXT_COLOR), (20, 50))
            self.screen.blit(self.menu.font.render(f"Total: {self.total_score + self.score}", True, TEXT_COLOR),(20, 80))

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


if __name__ == "__main__":
    game = Game()
    game.run()
