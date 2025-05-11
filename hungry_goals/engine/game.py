import pygame
import os
import math
import time
import random

from pygame import mouse

from hungry_goals.engine.config import *
from hungry_goals.utils import *
from hungry_goals.engine.window import Fenetre
from hungry_goals.entities.player1 import*
from hungry_goals.entities.player2 import*
from hungry_goals.entities.ball import Ball
from hungry_goals.entities.hoop import Panier
from hungry_goals.entities.arrow import Arrow
from hungry_goals.interfaces.menu_screen import MenuScreen
from hungry_goals.engine.backgroung import BackgroundManager
from hungry_goals.interfaces.screen import Ecran
from hungry_goals.interfaces.option_screen import OptionScreen
from hungry_goals.interfaces.player_selection import ChoixJoueur
from hungry_goals.engine.music_manager import MusicManager
from hungry_goals.engine.score_manager import ScoreManager
from hungry_goals.entities.bonus_item import BonusItem

class Game:
    # Classe principale du jeu : gère l'initialisation, la boucle principale, et la réinitialisation du jeu.

    def __init__(self):
        """
        Initialise le jeu et ses principaux attributs : fenêtre, ressources, état du jeu, objets, musique, etc.
        """
        pygame.init()

        # Initialisation de la fenêtre, police, et affichage
        self.window = Fenetre("Hungry Goals")
        self.screen = self.window.get_screen()
        self.font = pygame.font.SysFont("comicsans", 30)

        # Chargement des images et du fond
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        icon_path = os.path.join(base_path, "assets", "image", "logo.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        background_path = os.path.join(base_path, "assets", "image", "background.png")
        self.background = BackgroundManager(background_path, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Écrans et chargement
        self.ecran = Ecran(self.screen)
        self.ecran.show_loading_screen()

        # Horloge et temps de départ
        self.start_time = time.time()
        self.clock = pygame.time.Clock()

        # Joueur actif (sera défini selon le choix)
        self.player = None

        # Objets principaux du jeu
        self.player1 = Player1(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
        self.player2 = Player2(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
        self.arrow = Arrow()
        self.panier = Panier()
        self.menu = MenuScreen()
        self.option_screen = OptionScreen()
        self.choix_joueur = ChoixJoueur()

        # Bonus et gestion du temps de spawn des bonus
        self.bonus_items = []
        self.last_bonus_spawn = time.time()

        # États du jeu et variables de progression
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

        # Gestion du score et de la musique
        self.score_manager = ScoreManager()
        self.high_score = self.score_manager.load_high_score()



        music_path = os.path.join("assets", "sounds", "musique1.mp3")
        # Crée un objet qui va gérer la musique du jeu
        self.music = MusicManager(music_path)
        self.music.play()


    def run(self):
        """
        Boucle principale du jeu : gère les événements, l'affichage, la logique de gameplay, les menus et les états.
        """
        running = True

        while running:

            # Affiche un écran spécial "niveau final" pendant 2 secondes
            if self.final_screen_shown:
                # Si on est encore dans les 2 premières secondes après l'affichage
                if time.time() - self.final_screen_start < 2:

                    # Affiche l'image de transition
                    image_path = os.path.join("assets", "image", "niveau_finale.png")

                    challenge_img = pygame.image.load(image_path)
                    challenge_img = pygame.transform.scale(challenge_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # adapte la taille si besoin

                    self.screen.blit(challenge_img, challenge_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
                    pygame.display.flip()
                    self.clock.tick(60)
                    continue

                else:
                    # Fin de l'écran de transition : active le mode challenge
                    self.final_screen_shown = False
                    self.challenge_mode = True # On passe au mode challenge
                    self.start_time = time.time() # Redémarre le chrono
                    self.total_score = self.score   # On sauvegarde le score avant challenge
                    self.score = 0 # On remet à zéro pour la suite
                    self.score_challenge = 0 # Démarre un score spécial (si utilisé)
                    self.ball_list.clear() # Supprime les balles précédentes
                    self.panier.repositionner() # Repositionne le panier
                    continue

            # Affiche le menu des options (musique, sons, retour)
            if self.option:
                sound_btn_rect, music_btn_rect, back_btn_rect, rules_btn_rect = self.option_screen.draw(self.screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    # Ferme le jeu depuis l'écran d'options
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        # Si on clique sur le bouton du son
                        if sound_btn_rect.collidepoint(event.pos):
                            print("Sound button clicked")

                        # Pause ou reprend la musique
                        elif music_btn_rect.collidepoint(event.pos):
                            if pygame.mixer.music.get_busy():
                                self.music.pause()
                            else:
                                self.music.resume()

                        # Retour au menu principal
                        elif back_btn_rect.collidepoint(event.pos):
                            self.option = False

                        elif rules_btn_rect.collidepoint(event.pos):
                            # Charge l'image des règles
                            rules_image_path = os.path.join("assets", "image", "rules.png")
                            rules_image = pygame.image.load(rules_image_path)
                            rules_image = pygame.transform.scale(rules_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

                            # Définir la zone cliquable correspondant au bouton "Retour" DANS l'image
                            # (ajuste ces valeurs à la position réelle de ton bouton dans l'image)
                            return_click_zone = pygame.Rect(385, 540, 220, 40)



                            viewing_rules = True
                            while viewing_rules:
                                self.screen.blit(rules_image, (0, 0))
                                pos = mouse.get_pos()
                                afficher_texte(self.screen, self.font, f'pos : {pos}', (0, 0), 'white')
                                pygame.display.flip()

                                for e in pygame.event.get():
                                    if e.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                        pygame.quit()
                                        exit()
                                    elif e.type == pygame.MOUSEBUTTONDOWN :
                                        if return_click_zone.collidepoint(e.pos):
                                            viewing_rules = False


                self.clock.tick(60)
                continue

            # Affiche l'écran de sélection du joueur (Axel ou Tyson)
            if self.afficher_choix_joueur:
                axel_rect, tyson_rect, retour_rect = self.choix_joueur.draw(self.screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    # Fermer le jeu depuis cet écran
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        # Choix du joueur Axel
                        if axel_rect.collidepoint(event.pos):
                            self.start_time = time.time()
                            self.game_started = True
                            self.afficher_choix_joueur = False
                            self.player2 = Player2(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                            self.player = self.player2

                        # Choix du joueur Tyson
                        elif tyson_rect.collidepoint(event.pos):
                            self.start_time = time.time()
                            self.game_started = True
                            self.afficher_choix_joueur = False
                            self.player1 = Player1(random.randint(100, 3 * SCREEN_WIDTH // 4), PLAYER_Y)
                            self.player = self.player1

                        # Retour sans sélection : empêche de lancer le jeu sans joueur
                        elif retour_rect.collidepoint(event.pos):
                            self.start_time = None
                            self.afficher_choix_joueur = False
                            self.game_started = False
                            self.player = None  # évite le crash si aucun joueur sélectionné
                continue

            # Affiche le menu principal du jeu (jouer, options, quitter)
            if not self.game_started:
                jouer_btn, options_btn, quitter_btn = self.menu.draw_start_screen(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                pygame.display.flip()

                for event in pygame.event.get():
                    # Quitte le jeu depuis le menu
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if jouer_btn.collidepoint(event.pos):
                            self.afficher_choix_joueur = True  # Ouvre l'écran de choix du joueur

                        elif options_btn.collidepoint(event.pos):
                            self.option = True  # Ouvre les options

                        elif quitter_btn.collidepoint(event.pos):
                            self.total_score = 0
                            self.score = 0
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            pygame.quit()
                            exit()


            # Affiche l'écran de fin de partie avec les scores et options
            if self.game_over:
                btn_menu, btn_rejouer = self.menu.draw_game_over(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.total_score + self.score,self.high_score)
                pygame.display.flip()

                # Quitte le jeu depuis l'écran Game Over
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        total = self.total_score + self.score
                        if total > self.high_score:
                            self.score_manager.save_high_score(total)
                            self.high_score = total
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Sauvegarde du nouveau record si nécessaire
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
                            # Retour au menu principal
                            self.total_score = 0
                            self.score = 0
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            self.start_time = None
                            self.game_over = False
                            self.game_started = False
                            self.player = None

                        elif btn_rejouer.collidepoint(event.pos):
                            # Redémarre une nouvelle partie
                            self.total_score = 0
                            self.score = 0
                            total = self.total_score + self.score
                            if total > self.high_score:
                                self.score_manager.save_high_score(total)
                                self.high_score = total
                            self.reset_game()

                self.clock.tick(60)
                continue


            # Partie principale du gameplay : gestion du temps, des entrées, de la physique, des collisions, de l'affichage

            # Si la partie n'a pas encore commencé, on attend le lancement
            if not self.start_time:  # On attend que la partie commence
                continue

            # Calcul du temps écoulé et du temps restant avant la fin de la partie
            elapsed = time.time() - self.start_time  # Temps écoulé depuis le début de la partie
            remaining = max(0, int(TEMPS_JEU - elapsed))  # Temps restant avant la fin (jamais négatif)

            # Si le temps est écoulé, la partie est terminée
            if remaining <= 0:  # Partie terminée si temps écoulé
                total = self.total_score + self.score
                if total > self.high_score:
                    self.score_manager.save_high_score(total)
                    self.high_score = total
                    self.is_new_record = True

                # Passage en mode challenge si le score est suffisant et qu'on n'est pas déjà en challenge
                if self.score >= 12 and not self.challenge_mode:
                    self.final_screen_shown = True
                    self.final_screen_start = time.time()
                    continue

                self.game_over = True
                continue

            self.background.draw(self.screen)


            # Affichage du chrono
            chrono_text = self.menu.font.render(f"Time: {remaining}", True, TEXT_COLOR)
            self.screen.blit(chrono_text, chrono_text.get_rect(center=(SCREEN_WIDTH // 2, 20)))
            if remaining <= 3:
                txt = self.menu.huge_font.render(str(remaining), True, (255, 0, 255))
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))


            # Gestion des entrées clavier et souris
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, SCREEN_WIDTH)
            if keys[pygame.K_RETURN] and self.player.state != "special":
                self.player.start_special()


            # Gestion des événements (clavier, souris, fermeture, etc.)
            for event in pygame.event.get():  # Parcours tous les événements pygame (clavier, souris, etc.)

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    total = self.total_score + self.score
                    if total > self.high_score:
                        self.score_manager.save_high_score(total)
                        self.high_score = total
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_pos = pygame.mouse.get_pos()  # On enregistre la position de départ du tir (clic souris)
                    self.dragging = True
                    self.player.start_shoot()

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    current_mouse = pygame.mouse.get_pos()
                    dx = self.start_pos[0] - current_mouse[0]
                    dy = self.start_pos[1] - current_mouse[1]
                    self.preview_angle = math.atan2(dy, dx)  # Calcule l'angle du tir selon le déplacement souris
                    self.preview_power = min(math.hypot(dx, dy) / 5, 24)  # Calcule la puissance du tir (distance du drag)

                elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
                    end_pos = pygame.mouse.get_pos()  # On enregistre la position de fin du tir (relâchement souris)
                    self.player.state = "idle"
                    self.player.frames = self.player.frames_idle
                    self.player.frame_index = 0
                    if self.start_pos and self.start_pos != end_pos:
                        player_pos = self.player.get_position()
                        dx = self.start_pos[0] - end_pos[0]
                        dy = self.start_pos[1] - end_pos[1]
                        angle = math.atan2(dy, dx)  # Calcule l'angle du tir selon le vecteur souris (départ-arrivée)
                        power = min(math.hypot(dx, dy) / 5, 24)  # Calcule la puissance (distance de drag)
                        self.ball_list.append(Ball(player_pos[0], player_pos[1], angle, power))
                    self.dragging = False
                    self.start_pos = None
                    self.preview_angle = None
                    self.preview_power = None


            # Affichage du joueur, panier, et gestion du tir spécial
            self.player.draw(self.screen)
            self.panier.draw(self.screen)
            if self.player.shooting_done and self.player.state == "special":
                player_pos = self.player.get_position()
                _, _, hoop_rect = self.panier.get_rects()
                target_pos = hoop_rect.center
                dx = target_pos[0] - player_pos[0] * 0.8
                dy = target_pos[1] - player_pos[1] - 1500
                angle = math.atan2(dy, dx)
                power = 25
                self.ball_list.append(Ball(player_pos[0], player_pos[1], angle, power))
                self.player.state = "idle"


            # --- Affichage de la flèche de visée pendant le drag ---
            # Affiche une flèche qui indique la direction et la puissance du tir lorsque le joueur maintient le clic et vise.
            # Cela aide le joueur à anticiper la trajectoire de la balle avant de tirer.
            if self.dragging and self.start_pos:
                current_mouse_pos = pygame.mouse.get_pos()
                player_pos = self.player.get_position()
                if self.preview_angle is not None and self.preview_power is not None:
                    self.arrow.draw_trajectory(self.screen, player_pos, self.preview_angle, self.preview_power)


            # --- Boucle de mise à jour des balles, gestion du score et effets ---
            # Pour chaque balle active, on met à jour sa position, on vérifie les collisions avec le panier,
            # et on gère le score, le repositionnement du panier, et les effets spéciaux éventuels.
            backboard_rect, basket_rect, hoop_center_rect = self.panier.get_rects()

            for ball in self.ball_list:
                if ball.active:
                    result = ball.update(GRAVITY, SCREEN_HEIGHT, backboard_rect, basket_rect, hoop_center_rect)

                    if result == "score":
                        self.score += POINT_SCORE  # Incrémente le score si la balle marque
                        self.panier.repositionner()  # Repositionne le panier après chaque panier marqué
                        player_x = random.randint(100, 750)

                        # --- Effet de secousse pendant le mode challenge ---
                        # Lorsqu'un panier est marqué en mode challenge, la scène "tremble" pour ajouter du dynamisme.
                        if self.challenge_mode:
                            self.player.x = random.randint(100, 750)

                            for i in range(10):
                                intensity = max(1, 6 - i)
                                offset_x = random.randint(-intensity, intensity)
                                offset_y = random.randint(-intensity, intensity)
                                self.background.draw(self.screen)
                                self.screen.scroll(offset_x, offset_y)
                                self.player.draw(self.screen)
                                self.panier.draw(self.screen)
                                for b in self.ball_list:
                                    b.draw(self.screen)
                                pygame.display.flip()
                                self.clock.tick(60)

                    ball.draw(self.screen)
            # On ne conserve que les balles encore actives (pas rentrées ni hors écran)
            self.ball_list = [b for b in self.ball_list if b.active]



            # --- Mode challenge : repositionnement du panier et apparition de bonus ---
            # En mode challenge, le panier se repositionne automatiquement toutes les 2 secondes,
            # et un bonus apparaît toutes les 5 secondes à l'écran.
            if self.challenge_mode:
                if time.time() - self.challenge_timer > 2:
                    self.panier.repositionner()
                    self.challenge_timer = time.time()

                if time.time() - self.last_bonus_spawn > 5:
                    bonus = BonusItem("assets/image/bonus.png", SCREEN_WIDTH)
                    self.bonus_items.append(bonus)
                    self.last_bonus_spawn = time.time()



            # --- Système de bonus : gestion des collisions et suppression ---
            # Affiche les bonus, vérifie si le joueur les ramasse (collision), et les retire du jeu si besoin.
            # Si le joueur ramasse un bonus, il gagne du temps supplémentaire.
            for bonus in self.bonus_items:
                bonus.update()
                bonus.draw(self.screen)

                if self.player.rect.colliderect(bonus.rect):
                    self.start_time += TEMPS_ADDITIONNEL  # Ajoute du temps si bonus ramassé
                    self.bonus_items.remove(bonus)

            # Supprime les bonus qui sont sortis de l'écran
            self.bonus_items = [b for b in self.bonus_items if not b.is_off_screen(SCREEN_HEIGHT)]


            # Affichage du score, record, total
            self.screen.blit(self.menu.font.render(f"Score: {self.score}", True, TEXT_COLOR), (20, 20))
            record = self.score_manager.load_high_score()
            self.screen.blit(self.menu.font.render(f"Record: {record}", True, TEXT_COLOR), (20, 50))
            self.screen.blit(self.menu.font.render(f"Total: {self.total_score + self.score}", True, TEXT_COLOR),(20, 80))


            if not self.challenge_mode:
                objectif_text = self.menu.font.render(f"Objectif: 12", True, 'red')
                self.screen.blit(objectif_text, objectif_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def reset_game(self):
        """
        Réinitialise l'état du jeu pour recommencer une partie.
        """
        self.ball_list = []
        self.score = 0
        self.start_time = time.time()
        self.dragging = False
        self.start_pos = None
        self.game_started = True
        self.game_over = False
        self.challenge_mode = False
        self.total_score = 0
        self.bonus_items = []


if __name__ == "__main__":
    game = Game()
    game.run()
