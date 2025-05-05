import pygame
#

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
