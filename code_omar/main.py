import pygame
import math
import time
import random
import sys
import os

pygame.init()

# Configuration
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASKET_COLOR = (255, 100, 100)
BACKBOARD_COLOR = (100, 100, 100)
PLAYER_Y = HEIGHT - 100
GRAVITY = 0.5
PLAYER_SPEED = 5
ARCEAU_COLOR = (204, 0, 204)        # Rouge vif
PANNEAU_COLOR = (46, 46, 184)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Goals")
icon = pygame.image.load("assets/image/logo.png")
pygame.display.set_icon(icon)

font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 48)
font_huge = pygame.font.SysFont(None, 120)

# Police style pixel art (ex: pour le score affiché dans le menu)
pixel_font = pygame.font.Font(None, 48)  # Remplace None par le chemin si tu utilises une .ttf custom

# Gestion des scores
def load_high_scores(path="high_scores.txt"):
    if not os.path.exists(path):
        return 0
    with open(path, "r") as f:
        line = f.readline().strip()
        return int(line) if line.isdigit() else 0

def save_high_score(score, path="high_scores.txt"):
    with open(path, "w") as f:
        f.write(f"{score}\n")


# Chargement de sprites
def load_frames(sheet, row, num_frames, width, height, scale=3):
    return [pygame.transform.scale(
        sheet.subsurface(pygame.Rect(i * width, row * height, width, height)),
        (width * scale, height * scale)
    ) for i in range(num_frames)]

# Ecrans
def show_loading_screen():
    bg = pygame.image.load("assets/image/chargement.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    loading_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 20)
    bar_color = (255, 0, 255)  # rose néon

    for i in range(0, 301, 5):  # remplissage progressif
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (50, 0, 50), loading_rect)  # fond sombre
        pygame.draw.rect(screen, bar_color, (loading_rect.x, loading_rect.y, i, loading_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), loading_rect, 2)  # contour blanc
        pygame.display.flip()
        pygame.time.delay(30)  # vitesse de chargement simulée




def draw_start_screen():
    bg = pygame.image.load("assets/image/menu.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    jouer_btn = pygame.Rect(330, 220, 305, 65)
    options_btn = pygame.Rect(345, 305, 280, 50)
    quitter_btn = pygame.Rect(370, 380, 230, 45)

    # Zone du record
    record_rect = pygame.Rect(405, 448, 167, 42)

    # Recharge le meilleur score à chaque affichage
    if os.path.exists("high_scores.txt"):
        with open("high_scores.txt", "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
            if scores:
                best_score = max(scores)
                text_surface = pixel_font.render(f"Record : {best_score}", True, (0, 255, 255))
                text_rect = text_surface.get_rect(center=record_rect.center)
                screen.blit(text_surface, text_rect)

    return jouer_btn, options_btn, quitter_btn



def draw_option_screen():
    bg = pygame.image.load("assets/image/option_screen.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    return pygame.Rect(400, 230, 220, 60), pygame.Rect(400, 330, 220, 60), pygame.Rect(400, 430, 220, 60)

def draw_choix_joueur_screen():
    bg = pygame.image.load("assets/image/choix_joueur.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    # Rectangles cliquables selon les coordonnées fournies
    retour_btn = pygame.Rect(46, 39, 201, 59)               # Bouton RETOUR
    tyson_btn = pygame.Rect(164, 162, 282, 349)             # Zone de Tyson
    axel_btn = pygame.Rect(552, 159, 286, 351)              # Zone d'Axel

    return tyson_btn, axel_btn, retour_btn


def draw_game_over(score, high_score, is_record=False):
    if is_record:
        bg = pygame.image.load("assets/image/you_win.png").convert()
    elif score < 10:
        bg = pygame.image.load("assets/image/game_over.png").convert()
    else:
        screen.fill(WHITE)
        screen.blit(font_big.render("Game Over", True, BLACK), (WIDTH // 2 - 80, HEIGHT // 2 - 120))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (WIDTH // 2 - 50, HEIGHT // 2 - 60))
        screen.blit(font.render(f"Best Record: {high_score}", True, BLACK), (WIDTH // 2 - 70, HEIGHT // 2 + 20))
        # bouton replay
        btn = pygame.Rect(WIDTH - 160, HEIGHT - 80, 140, 50)
        pygame.draw.rect(screen, (200, 200, 200), btn)
        pygame.draw.rect(screen, BLACK, btn, 2)
        screen.blit(font.render("Replay", True, BLACK), font.render("Replay", True, BLACK).get_rect(center=btn.center))
        return btn

    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    btn = pygame.Rect(WIDTH - 160, HEIGHT - 80, 140, 50)
    pygame.draw.rect(screen, (200, 200, 200), btn)
    pygame.draw.rect(screen, BLACK, btn, 2)
    screen.blit(font.render("Replay", True, BLACK), font.render("Replay", True, BLACK).get_rect(center=btn.center))
    return btn




def detect_colored_rect(image, target_color):
    """Renvoie un pygame.Rect englobant tous les pixels ayant la couleur spécifiée."""
    mask = pygame.mask.from_threshold(image, target_color, (1, 1, 1, 255))
    if mask.count() == 0:
        return None
    return mask.get_bounding_rects()[0]

def draw_trajectory(surface, start_pos, angle, power, steps=20):
    # Clone exact de la logique de Ball.__init__
    x = float(start_pos[0])
    y = float(start_pos[1])
    vel_x = math.cos(angle) * power
    vel_y = math.sin(angle) * power
    radius = BALL_RADIUS

    for _ in range(steps):
        # Mise à jour position
        x += vel_x
        y += vel_y

        # Affichage du point
        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
            pygame.draw.circle(surface, (200, 0, 200), (int(x), int(y)), 4)
        else:
            break

        # Gravité identique à Ball.update()
        vel_y += GRAVITY

        # Rebond identique au sol
        if y + radius >= HEIGHT:
            y = HEIGHT - radius
            if abs(vel_y) > 1:
                vel_y *= -0.5
                vel_x *= 0.95
            else:
                break  # balle au sol, arrêt

        # Rebond gauche/droite identique
        if x - radius <= 0:
            x = radius
            vel_x *= -0.8
        elif x + radius >= WIDTH:
            x = WIDTH - radius
            vel_x *= -0.8



# Ball
class Ball:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        self.vel_x = math.cos(angle) * power
        self.vel_y = math.sin(angle) * power
        self.active = True
        self.rest_time = None
        self.scored = False

    def update(self):
        if not self.active:
            return
        self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y + BALL_RADIUS >= HEIGHT:
            self.y = HEIGHT - BALL_RADIUS
            if abs(self.vel_y) > 1:
                self.vel_y *= -0.5
                self.vel_x *= 0.95
            else:
                self.vel_y = 0
                self.vel_x = 0
                if self.rest_time is None:
                    self.rest_time = time.time()

        # Rebond côté gauche
        if self.x - BALL_RADIUS <= 0:
            self.x = BALL_RADIUS
            self.vel_x *= -0.8  # rebond plus doux
            self.vel_y *= 0.95  # légère perte d’énergie

        # Rebond côté droit
        elif self.x + BALL_RADIUS >= WIDTH:
            self.x = WIDTH - BALL_RADIUS
            self.vel_x *= -0.8
            self.vel_y *= 0.95

        if self.rect().colliderect(backboard_rect):
            self.x -= self.vel_x
            self.vel_x *= -0.7
        if self.rect().colliderect(basket_rect):
            self.x -= self.vel_x
            self.vel_x *= -0.6
        if self.rect().colliderect(hoop_center_rect) and self.vel_y > 0 and not self.scored:
            self.active = False
            self.scored = True
            return "score"
        if self.rest_time and time.time() - self.rest_time > 1.5:
            self.active = False

    def draw(self, surface):
        surface.blit(ball_image, (int(self.x - BALL_RADIUS), int(self.y - BALL_RADIUS)))

    def rect(self):
        return pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)


def reposition_panier():

    min_y = 200  # ← pour ne pas être collé en haut
    max_y = int(HEIGHT * 0.75)  # ← moitié de l'écran : 300 si HEIGHT = 600
    y = random.randint(min_y, max_y)

    # Dimensions
    basket_width = 70
    basket_height = 10
    backboard_width = 10
    backboard_height = 70
    hoop_width = 50
    hoop_height = 12

    # Repositionner
    global basket_rect, backboard_rect, hoop_center_rect
    basket_rect = pygame.Rect(WIDTH - 80, y, basket_width, basket_height)
    backboard_rect = pygame.Rect(
        basket_rect.right - backboard_width,
        basket_rect.top - backboard_height + 10,
        backboard_width,
        backboard_height
    )
    hoop_center_rect = pygame.Rect(
        basket_rect.centerx - hoop_width // 2,
        basket_rect.bottom,
        hoop_width,
        hoop_height
    )

# Panier : initialise une première position dynamique
reposition_panier()

# Balle
ball_image = pygame.image.load("assets/image/Ball.png").convert_alpha()
ball_image = pygame.transform.scale(ball_image, (50, 50))
BALL_RADIUS = ball_image.get_width() // 2

background_game = pygame.image.load("assets/image/terrain.png").convert()
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))


def main():
    show_loading_screen()
    clock = pygame.time.Clock()
    high_score = load_high_scores()

    current_player = None
    on_option_screen = False
    on_choix_joueur = False
    game_started = False
    game_over = False
    frame_index = 0
    score = 0
    ball_list = []
    dragging = False
    start_pos = None
    preview_angle = None
    preview_power = None
    start_time = None
    is_new_record = False
    player_x = random.randint(100, 750)

    running = True

    while running:

        # Écran des options
        if on_option_screen:
            music_btn, sound_btn, return_btn = draw_option_screen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if music_btn.collidepoint(event.pos):
                        print("🎵 Musique toggle")
                    elif sound_btn.collidepoint(event.pos):
                        print("🔊 Son toggle")
                    elif return_btn.collidepoint(event.pos):
                        on_option_screen = False
            clock.tick(60)
            continue

        # Écran choix joueur
        if on_choix_joueur:
            tyson_btn, axel_btn, retour_btn = draw_choix_joueur_screen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if tyson_btn.collidepoint(event.pos):
                        current_player = "tyson"
                        sprite_sheet = pygame.image.load("assets/image/Character.png").convert_alpha()
                        on_choix_joueur = False
                        game_started = True
                        start_time = time.time()
                    elif axel_btn.collidepoint(event.pos):
                        current_player = "axel"
                        sprite_sheet = pygame.image.load("assets/image/Character2.png").convert_alpha()
                        on_choix_joueur = False
                        game_started = True
                        start_time = time.time()
                    elif retour_btn.collidepoint(event.pos):
                        on_choix_joueur = False
            clock.tick(60)
            continue

        # Menu principal
        if not game_started:
            jouer_btn, options_btn, quitter_btn = draw_start_screen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if jouer_btn.collidepoint(event.pos):
                        on_choix_joueur = True
                    elif options_btn.collidepoint(event.pos):
                        on_option_screen = True
                    elif quitter_btn.collidepoint(event.pos):
                        save_high_score(high_score)
                        pygame.quit()
                        sys.exit()
            clock.tick(60)
            continue

        # Écran de fin
        if game_over:
            btn = draw_game_over(score, high_score, is_new_record)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos):
                    if score > high_score:
                        high_score = score
                        save_high_score(score)

                    score = 0
                    ball_list.clear()
                    game_started = False
                    game_over = False
                    player_x = random.randint(100, 750)
            clock.tick(60)
            continue

        # Partie en cours
        elapsed = time.time() - start_time
        remaining = max(0, int(60 - elapsed))
        if remaining <= 0:
            if score > high_score:
                save_high_score(score)
                is_new_record = True
                high_score = score
            game_over = True
            continue

        # Chargement des frames
        if current_player:
            if current_player == "tyson":
                frames_idle = load_frames(sprite_sheet, 2, 23, 64, 64)
                frames_run = load_frames(sprite_sheet, 8, 7, 64, 64) + load_frames(sprite_sheet, 9, 20, 64, 64)
            elif current_player == "axel":
                frames_idle = load_frames(sprite_sheet, 2, 23, 64, 64)
                frames_run = load_frames(sprite_sheet, 8, 7, 64, 64) + load_frames(sprite_sheet, 9, 20, 64, 64)
            frames_left = [pygame.transform.flip(f, True, False) for f in frames_run]

        # Affichage principal
        screen.blit(background_game, (0, 0))
        screen.blit(font.render(f"Time: {remaining}", True, BLACK), (20, 20))
        if remaining <= 3:
            screen.blit(font_huge.render(str(remaining), True, BLACK), (WIDTH // 2 - 40, HEIGHT // 2 - 60))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED
            direction = "left"
        elif keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED
            direction = "right"
        else:
            direction = "idle"

        player_x = max(30, min(WIDTH - 30, player_x))
        frames = frames_left if direction == "left" else frames_run if direction == "right" else frames_idle
        frame_index += 0.3
        if frame_index >= len(frames):
            frame_index = 0
        current_frame = frames[int(frame_index)]
        player_y = PLAYER_Y
        player_pos = (player_x, player_y)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                dragging = True
            elif event.type == pygame.MOUSEMOTION and dragging:
                current_mouse = pygame.mouse.get_pos()
                dx = start_pos[0] - current_mouse[0]
                dy = start_pos[1] - current_mouse[1]
                preview_angle = math.atan2(dy, dx)
                preview_power = min(math.hypot(dx, dy) / 5, 24)
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                end_pos = pygame.mouse.get_pos()
                dx, dy = start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]
                angle = math.atan2(dy, dx)
                power = min(math.hypot(dx, dy) / 5, 24)
                ball_list.append(Ball(player_x, player_y, angle, power))
                dragging = False
                preview_angle = None
                preview_power = None

        screen.blit(current_frame, (player_x - current_frame.get_width() // 2, player_y - current_frame.get_height() // 2))
        pygame.draw.rect(screen, ARCEAU_COLOR, basket_rect)
        pygame.draw.rect(screen, PANNEAU_COLOR, backboard_rect)

        # Boucle balle
        for ball in ball_list:
            if ball.active:
                if ball.update() == "score":
                    score += 1
                    reposition_panier()
                    player_x = random.randint(100, 750)
                ball.draw(screen)
        ball_list = [b for b in ball_list if b.active]

        # Dessin de la trajectoire prévisionnelle
        if dragging and preview_angle is not None and preview_power is not None:
            draw_trajectory(screen, player_pos, preview_angle, preview_power)

        screen.blit(font.render(f"Score: {score}", True, BLACK), (WIDTH - 200, 40))
        screen.blit(font.render(f"Record: {high_score}", True, BLACK), (WIDTH - 200, 10))
        screen.blit(font.render(f"Mouse: {pygame.mouse.get_pos()}", True, BLACK), (20, HEIGHT - 40))
        pygame.display.flip()
        clock.tick(60)

    save_high_score(high_score)
    pygame.quit()


if __name__ == "__main__":
    main()
