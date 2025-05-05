import pygame

SCALE = 3  # ou 3 pour encore plus grand

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (0, 100, 255)
        self.speed = 10
        self.frame_index = 0
        self.animation_speed = 0.4

        self.sprite_sheet = pygame.image.load("assets/image/Character.png").convert_alpha()

        self.frames_idle = self.load_frames(row=2, num_frames=23, width=64, height=64)  # immobile
        self.frames_right = self.load_frames(row=8, num_frames=7, width=64, height=64)  # dribble droite

        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]  # dribble gauche

        self.frames = self.frames_idle
        self.current_frame = self.frames_idle[self.frame_index]

    def load_frames(self, row, num_frames, width, height):
        frames = []
        for i in range(num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * width, row * height, width, height))
            frame = pygame.transform.scale(frame, (width * SCALE, height * SCALE))
            frames.append(frame)
        return frames

    def update_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.current_frame = self.frames[int(self.frame_index)]


    def handle_input(self, keys, screen_width):
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
            moving = False

        if moving:
            self.update_animation()
        else:
            self.update_animation()  # animation idle aussi

        self.x = max(self.radius, min(screen_width - self.radius, self.x))

    def draw(self, surface):
        surface.blit(self.current_frame, (self.x - self.current_frame.get_width() // 2, self.y - self.current_frame.get_height() // 2))

    def get_position(self):
        return (self.x, self.y)