import pygame



class game :
    def __init__(self):
        self.longueur, self.largeur = 850,600
        self.ecran = pygame.display.set_mode((self.largeur,self.largeur))
        self.titre = pygame.display.set_caption("Projet Transverse")


        pass

