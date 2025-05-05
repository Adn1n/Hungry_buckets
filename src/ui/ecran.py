import pygame
import time
import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
loading_path = os.path.join(base_path, "assets", "image", "ecran_chargement2.png")
loading_image = pygame.image.load(loading_path)

class Ecran:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = screen.get_size()

    def show_loading_screen(self):
        loading_image = pygame.image.load(loading_path)
        loading_image = pygame.transform.scale(loading_image, (self.WIDTH, self.HEIGHT))
        start_time = time.time()
        duration = 1  # secondes

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
            progress_width = int(400 * progress)

            # barre de chargement
            pygame.draw.rect(self.screen, (255, 255, 255), (220, 575, 400, 20), 2)
            pygame.draw.rect(self.screen, (255, 165, 0), (220, 575, progress_width, 20))

            pygame.display.flip()
            self.clock.tick(60)




