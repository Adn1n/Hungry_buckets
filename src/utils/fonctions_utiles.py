
def afficher_texte(ecran,font, texte, position, couleur):
    rendu = font.render(texte, True, couleur)
    ecran.blit(rendu, position)


def adapter_position(position_logique, taille_fenetre, taille_reference):
    """
    Convertit une position logique en pixels selon la taille actuelle de la fenêtre.

    :param position_logique: tuple (x, y) dans le monde logique
    :param taille_fenetre: tuple (largeur_actuelle, hauteur_actuelle)
    :param taille_reference: tuple (largeur_base, hauteur_base)
    :return: tuple (x_affiché, y_affiché)
    """
    x_logique, y_logique = position_logique
    largeur_fenetre, hauteur_fenetre = taille_fenetre
    largeur_base, hauteur_base = taille_reference

    scale_x = largeur_fenetre / largeur_base
    scale_y = hauteur_fenetre / hauteur_base

    x_affiche = x_logique * scale_x
    y_affiche = y_logique * scale_y

    return int(x_affiche), int(y_affiche)