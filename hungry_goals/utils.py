# Projet : Hungry Buckets
# Description : Fonctions utilitaires pour le projet : chargement de sprites, mise à jour d’animations, affichage de texte, détection de pixels colorés.

import pygame
import os
import time
import math

from hungry_goals.engine.config import *

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
image_path = os.path.join(base_path, "assets", "image", "Ball.png")

ball_image = pygame.image.load("assets/image/Ball.png")
ball_image = pygame.transform.scale(ball_image, (50, 50))
BALL_RADIUS = ball_image.get_width() // 2


def afficher_texte(ecran,font, texte, position, couleur):
    """
    Affiche un texte sur l'écran à une position donnée.

    Paramètres :
    - ecran : surface pygame sur laquelle afficher le texte
    - font : objet pygame.font.Font utilisé pour rendre le texte
    - texte : chaîne de caractères à afficher
    - position : tuple (x, y) indiquant la position d'affichage
    - couleur : couleur du texte (tuple RGB)

    Retour :
    - Aucun
    """
    rendu = font.render(texte, True, couleur)
    ecran.blit(rendu, position)


SCALE = 3  # à placer en haut si pas déjà défini

def load_frames(sprite_sheet, row, num_frames, width, height):
    """
    Charge une série de frames à partir d'une feuille de sprite.

    Paramètres :
    - sprite_sheet : surface pygame contenant la feuille de sprites
    - row : ligne dans la feuille de sprite à extraire
    - num_frames : nombre de frames à charger
    - width : largeur d'une frame
    - height : hauteur d'une frame

    Retour :
    - Liste de surfaces pygame correspondant aux frames chargées et mises à l'échelle
    """
    frames = []
    # Boucle de chargement de frames
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * width, row * height, width, height))
        # Application des transformations (scale)
        frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))
        frames.append(frame)
    return frames

def update_animation(frame_index, frames, animation_speed):
    """
    Met à jour l'index d'animation et retourne la frame correspondante.

    Paramètres :
    - frame_index : index flottant actuel de la frame d'animation
    - frames : liste des frames d'animation
    - animation_speed : vitesse d'animation (incrément de l'index)

    Retour :
    - tuple (nouvel index de frame, frame pygame correspondant)
    """
    # Calcul d’index
    frame_index += animation_speed
    if frame_index >= len(frames):
        frame_index = 0
    return frame_index, frames[int(frame_index)]

def load_combined_frames(sprite_sheet, rows, num_frames_per_row, width, height):
    """
    Charge des frames combinées à partir de plusieurs lignes d'une feuille de sprite.

    Paramètres :
    - sprite_sheet : surface pygame contenant la feuille de sprites
    - rows : liste des indices de lignes à extraire
    - num_frames_per_row : liste du nombre de frames par ligne
    - width : largeur d'une frame
    - height : hauteur d'une frame

    Retour :
    - Liste de surfaces pygame correspondant aux frames chargées et mises à l'échelle
    """
    frames = []
    # Boucle de chargement de frames pour chaque ligne
    for idx, row in enumerate(rows):
        for i in range(num_frames_per_row[idx]):
            frame = sprite_sheet.subsurface(pygame.Rect(i * width, row * height, width, height))
            # Application des transformations (scale)
            frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))
            frames.append(frame)
    return frames



