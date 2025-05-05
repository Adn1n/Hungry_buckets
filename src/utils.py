import pygame


def afficher_texte(ecran,font, texte, position, couleur):
    rendu = font.render(texte, True, couleur)
    ecran.blit(rendu, position)
