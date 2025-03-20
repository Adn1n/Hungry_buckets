import pygame


class game :
    def __init__(self):
        self.longueur, self.largeur = 850,600
        self.ecran = pygame.display.set_mode((self.largeur,self.largeur))
        pygame.display.set_caption("Projet Transverse")
        icone = pygame.image.load('tombereau.png')
        pygame.display.set_icon(icone)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.ecran.fill((0,0,230))
        pygame.display.update()

    def handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        return True

    def run(self):
        self.running = True
        while self.running :
            self.handling()
            self.draw()
            self.clock.tick(60)


    pygame.quit()


game = game()
game.run()

