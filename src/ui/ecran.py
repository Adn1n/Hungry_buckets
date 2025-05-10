import pygame
import time

from src.utils import *
import os

#
class Ecran:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = screen.get_size()

    def show_loading_screen(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(base_path, "assets", "image", "chargement.png")
        loading_image = pygame.image.load(image_path)
        loading_image = pygame.transform.scale(loading_image, (self.WIDTH, self.HEIGHT))
        start_time = time.time()
        duration = 1 # secondes

        font = pygame.font.SysFont("arial", 30)

        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE :
                        pygame.quit()
                        exit()


            self.screen.fill((0, 0, 0))
            self.screen.blit(loading_image, (0, 0))

            progress = (time.time() - start_time) / duration
            progress_width = int(515 * progress)


            pos = pygame.mouse.get_pos()
            afficher_texte(self.screen, font, f'pos : {pos[0],pos[1]}', (0,0), "white")
            # barre de chargement
            pygame.draw.rect(self.screen, (255, 255, 255), (270, 515, 515, 15), 2)
            pygame.draw.rect(self.screen, (0, 255, 255), (270, 515, progress_width, 15))

            pygame.display.flip()
            self.clock.tick(60)




