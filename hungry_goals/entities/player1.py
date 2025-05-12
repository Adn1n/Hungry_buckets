# Projet : Hungry Buckets
# Description : Ce fichier contient la classe Player1, qui gère les animations, mouvements, et actions du personnage joueur 1.

import pygame
from hungry_goals.utils import *
import os
#
SCALE = 3  # ou 3 pour encore plus grand

class Player1:
    def __init__(self, x, y):
        """
        Initialise un objet Player1 avec sa position, ses propriétés et ses animations.

        Paramètres :
        - self : instance de la classe Player1
        - x (int) : position horizontale initiale du joueur
        - y (int) : position verticale initiale du joueur

        Retour : None
        """
        # Initialisation des attributs de position et animation
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 100, 255)
        self.speed = 6
        self.frame_index = 0
        self.animation_speed = 0.4

        # Chargement de la sprite sheet
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "Character.png")
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Chargement des différentes animations (idle, right, left, shoot, special)
        self.frames_idle = load_frames(self.sprite_sheet, row=2, num_frames=23, width=64, height=64)
        self.frames_right = load_combined_frames(self.sprite_sheet, rows=[8, 9], num_frames_per_row=[7, 20], width=64,height=64)
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]  # dribble gauche

        self.frames_shoot = load_frames(self.sprite_sheet,3, 5, width=64, height=64)
        self.frames_special = load_frames(self.sprite_sheet, row=7, num_frames=11, width=64, height=64)

        # Initialisation de l’état et frame actuelle
        self.state = "idle"
        self.shooting_done = False

        self.frames = self.frames_idle
        self.current_frame = self.frames_idle[self.frame_index]

    def start_shoot(self):
        """
        Démarre l'animation de tir si le joueur n'est pas déjà en train de tirer.

        Paramètres :
        - self : instance de la classe Player1

        Retour : None
        """
        if self.state != "shoot":
            self.frames = self.frames_shoot
            self.frame_index = 0
            self.state = "shoot"
            self.shooting_done = False

    def start_special(self):
        """
        Démarre l'animation spéciale si le joueur n'est pas déjà en animation spéciale.

        Paramètres :
        - self : instance de la classe Player1

        Retour : None
        """
        if self.state != "special":
            self.frames = self.frames_special
            self.frame_index = 0
            self.state = "special"
            self.shooting_done = False

    def handle_input(self, keys, screen_width):
        """
        Gère les entrées clavier pour déplacer le joueur ou lancer des animations.

        Paramètres :
        - self : instance de la classe Player1
        - keys : liste ou dictionnaire des touches pressées (ex : pygame.key.get_pressed())
        - screen_width (int) : largeur de l'écran pour limiter le déplacement horizontal

        Retour : None
        """

        # Si une animation de tir ou spéciale est en cours, on la joue jusqu'au bout sans interruption
        if self.state in ["shoot", "special"]:
            if not self.shooting_done:
                # Met à jour l'animation image par image
                self.frame_index, self.current_frame = update_animation(self.frame_index, self.frames,
                                                                        self.animation_speed)
                if int(self.frame_index) >= len(self.frames) - 1:
                    # Arrête l'animation à la dernière image
                    self.frame_index = len(self.frames) - 1
                    self.current_frame = self.frames[self.frame_index]
                    self.shooting_done = True
            return  # On ne gère pas les déplacements pendant ces animations

        moving = False  # Sert à détecter si le joueur bouge

        # Gestion du déplacement vers la gauche
        if keys[pygame.K_LEFT]:
            if self.frames != self.frames_left:
                self.frames = self.frames_left  # Active l'animation correspondante
                self.frame_index = 0
            self.x -= self.speed
            moving = True

        # Gestion du déplacement vers la droite
        elif keys[pygame.K_RIGHT]:
            if self.frames != self.frames_right:
                self.frames = self.frames_right
                self.frame_index = 0
            self.x += self.speed
            moving = True

        # Si aucune touche directionnelle n’est pressée : on revient à l’état "idle"
        else:
            if self.frames != self.frames_idle:
                self.frames = self.frames_idle
                self.frame_index = 0

        # Mise à jour de l'animation (idle ou déplacement)
        self.frame_index, self.current_frame = update_animation(self.frame_index, self.frames, self.animation_speed)

        # Empêche le joueur de sortir de l'écran horizontalement
        self.x = max(self.radius, min(screen_width - self.radius, self.x))


    def draw(self, surface):
        """
        Dessine le joueur sur la surface donnée.

        Paramètres :
        - self : instance de la classe Player1
        - surface : surface pygame sur laquelle dessiner le joueur

        Retour : None
        """
        self.rect = self.current_frame.get_rect(center=(self.x, self.y))
        surface.blit(self.current_frame, self.rect)


    def get_position(self):
        """
        Retourne la position actuelle du joueur.

        Paramètres :
        - self : instance de la classe Player1

        Retour :
        - tuple (x, y) : position actuelle du joueur
        """
        return (self.x, self.y)