import pygame
import os
import time
import math

from src.core.config import *
#



base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
image_path = os.path.join(base_path, "assets", "image", "Ball.png")

ball_image = pygame.image.load("assets/image/Ball.png")
ball_image = pygame.transform.scale(ball_image, (50, 50))
BALL_RADIUS = ball_image.get_width() // 2


def afficher_texte(ecran,font, texte, position, couleur):
    rendu = font.render(texte, True, couleur)
    ecran.blit(rendu, position)


SCALE = 3  # à placer en haut si pas déjà défini

def load_frames(sprite_sheet, row, num_frames, width, height):
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * width, row * height, width, height))
        frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))
        frames.append(frame)
    return frames

def update_animation(frame_index, frames, animation_speed):
    frame_index += animation_speed
    if frame_index >= len(frames):
        frame_index = 0
    return frame_index, frames[int(frame_index)]

def load_combined_frames(sprite_sheet, rows, num_frames_per_row, width, height):
    frames = []
    for idx, row in enumerate(rows):
        for i in range(num_frames_per_row[idx]):
            frame = sprite_sheet.subsurface(pygame.Rect(i * width, row * height, width, height))
            frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))
            frames.append(frame)
    return frames


def load_high_scores(path="high_scores.txt"):
    if not os.path.exists(path):
        return 0
    with open(path, "r") as f:
        line = f.readline().strip()
        return int(line) if line.isdigit() else 0



def save_high_score(score, path="high_scores.txt"):
    if os.path.exists(path):
        with open(path, "r") as f:
            line = f.readline().strip()
            if line.isdigit() and int(line) >= score:
                return  # pas un nouveau record

    with open(path, "w") as f:
        f.write(f"{score}\n")

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
        if 0 <= x <= SCREEN_WIDTH and 0 <= y <= SCREEN_HEIGHT:
            pygame.draw.circle(surface, (200, 0, 200), (int(x), int(y)), 4)
        else:
            break

        # Gravité identique à Ball.update()
        vel_y += GRAVITY

        # Rebond identique au sol
        if y + radius >= SCREEN_HEIGHT:
            y = SCREEN_HEIGHT - radius
            if abs(vel_y) > 1:
                vel_y *= -0.5
                vel_x *= 0.95
            else:
                break  # balle au sol, arrêt

        # Rebond gauche/droite identique
        if x - radius <= 0:
            x = radius
            vel_x *= -0.8
        elif x + radius >= SCREEN_WIDTH:
            x = SCREEN_WIDTH - radius
            vel_x *= -0.8

