

import pygame
import math
import sys
import os


# Obtenir le chemin absolu du dossier courant
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets"))
# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trajectoire balle de basket")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Paramètres du lancer
gravity = 9.81 * 100  # pixels/s²
speed = 20  # force du tir
angle_deg = 45  # angle du tir
start_pos = (100, HEIGHT - 100)
ball_radius = 10

# Convertir angle et vitesse en composantes vx et vy
angle_rad = math.radians(angle_deg)
vx = speed * math.cos(angle_rad) * 50  # pixels/s
vy = -speed * math.sin(angle_rad) * 50  # pixels/s



# État
ball_pos = list(start_pos)
trajectory = []  # pour dessiner la trajectoire

# --- Animation du joueur ---
# Chargement des images du joueur
player_idle = pygame.image.load(os.path.join(BASE_PATH, "player_idle.png")).convert_alpha()
player_idle = pygame.transform.scale(player_idle, (60, 40))
player_run_images = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(BASE_PATH, "player_run1.png")).convert_alpha(), (60, 40)
    ),
]

# Position et état
player_x = 0
player_rect = player_idle.get_rect()
player_y = HEIGHT - player_rect.h


player_speed = 5
player_run_index = 0
player_run_timer = 0
animation_speed = 0.1  # secondes par frame


running = True
shooting = False
time_elapsed = 0

while running:
    dt = clock.tick(60) / 1000  # secondes
    screen.fill(WHITE)

    # --- Animation joueur ---
    keys = pygame.key.get_pressed()
    is_running = keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]

    if is_running:
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        elif keys[pygame.K_LEFT]:
            player_x -= player_speed

        # Animation de course
        current_time = pygame.time.get_ticks() / 1000
        if current_time - player_run_timer > animation_speed:
            player_run_timer = current_time
            player_run_index = (player_run_index + 1) % len(player_run_images)
        player_image = player_run_images[player_run_index]
    else:
        player_image = player_idle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ball_pos = list(start_pos)
            time_elapsed = 0
            shooting = True

    if shooting:
        time_elapsed += dt
        x = start_pos[0] + vx * time_elapsed
        y = start_pos[1] + vy * time_elapsed + 0.5 * gravity * time_elapsed ** 2
        ball_pos = [x, y]
        trajectory.append((int(x), int(y)))
        if y > HEIGHT:
            shooting = False

    # Dessin
    for point in trajectory:
        pygame.draw.circle(screen, ORANGE, point, 3)
    pygame.draw.circle(screen, ORANGE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Affichage du joueur
    screen.blit(player_image, (player_x, player_y))

    pygame.display.flip()

pygame.quit()
sys.exit()