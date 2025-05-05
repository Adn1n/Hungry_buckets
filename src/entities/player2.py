
import pygame
from src.utils import *
#
SCALE = 3  # ou 3 pour encore plus grand

class Player2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 100, 255)
        self.speed = 6
        self.frame_index = 0
        self.animation_speed = 0.4

        self.sprite_sheet = pygame.image.load("assets/image/Character2.png").convert_alpha()

        self.frames_idle = load_frames(self.sprite_sheet, row=2, num_frames=23, width=64, height=64)
        self.frames_right = load_combined_frames(self.sprite_sheet, rows=[8, 9], num_frames_per_row=[7, 20], width=64,height=64)
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]  # dribble gauche

        self.frames_shoot = load_frames(self.sprite_sheet,3, 5, width=64, height=64)
        self.state = "idle"
        self.shooting_done = False

        self.frames = self.frames_idle
        self.current_frame = self.frames_idle[self.frame_index]

    def start_shoot(self):
        if self.state != "shoot":
            self.frames = self.frames_shoot
            self.frame_index = 0
            self.state = "shoot"
            self.shooting_done = False


    def handle_input(self, keys, screen_width):
        if self.state == "shoot":
            if not self.shooting_done:
                self.frame_index, self.current_frame = update_animation(self.frame_index, self.frames,
                                                                        self.animation_speed)
                if int(self.frame_index) >= len(self.frames) - 1:
                    self.frame_index = len(self.frames) - 1
                    self.current_frame = self.frames[self.frame_index]
                    self.shooting_done = True
            return

        moving = False

        if keys[pygame.K_LEFT]:
            if self.frames != self.frames_left:
                self.frames = self.frames_left
                self.frame_index = 0
            self.x -= self.speed
            moving = True

        elif keys[pygame.K_RIGHT]:
            if self.frames != self.frames_right:
                self.frames = self.frames_right
                self.frame_index = 0
            self.x += self.speed
            moving = True

        else:
            if self.frames != self.frames_idle:
                self.frames = self.frames_idle
                self.frame_index = 0

        # Animation si déplacement ou idle
        self.frame_index, self.current_frame = update_animation(self.frame_index, self.frames, self.animation_speed)
        self.x = max(self.radius, min(screen_width - self.radius, self.x))


    def draw(self, surface):
        surface.blit(self.current_frame, (self.x - self.current_frame.get_width() // 2, self.y - self.current_frame.get_height() // 2))

    def get_position(self):
        return (self.x, self.y)