import pygame
import os

class MusicManager:
    def __init__(self, path, volume=0.5):
        pygame.mixer.init()
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
        else:
            print(f"[ERREUR] Fichier introuvable : {path}")

    def play(self, loop=True):
        # Joue la musique en boucle si loop est True (avec -1), sinon la joue une seule fois (avec 0)
        pygame.mixer.music.play(-1 if loop else 0)

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value)