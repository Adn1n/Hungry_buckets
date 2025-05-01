from src.entities.player import Player
from config import *
from src.utils.fonctions_utiles import *
from src.entities.arrow import Arrow


class Game:
    """Classe principale qui gère la boucle du jeu, l'affichage, les événements et l'état du joueur."""

    def __init__(self):
        pygame.init()  # Initialise tous les modules pygame
        self.ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)  # Crée une fenêtre redimensionnable avec les dimensions définies dans config.py
        pygame.display.set_caption("Projet Transverse")  # Définit le titre de la fenêtre
        icone = pygame.image.load('assets/image/icone_basket.png')  # Charge l'image utilisée comme icône de la fenêtre
        pygame.display.set_icon(icone)  # Définit l'icône de la fenêtre
        self.clock = pygame.time.Clock()  # Crée une horloge pour gérer le framerate

        self.reference_size = (1280, 720)  # Taille de référence pour l’affichage, potentiellement pour le redimensionnement futur

        self.player = Player(self.ecran)  # Initialise le joueur avec l’écran en paramètre

        self.background_original = pygame.image.load("assets/image/arriere_plan_basket.png")  # Charge le fond d’écran original
        self.background = pygame.transform.scale(self.background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionne l’image de fond à la taille de la fenêtre

        self.font = pygame.font.SysFont('arial', FONT_SIZE)  # Définit la police utilisée dans le jeu
        self.running = True  # Indique si le jeu est en cours d'exécution

    def creer_arrow(self,spawn):
        # Crée une nouvelle flèche à la position de spawn spécifiée
        self.arrow = Arrow(self.ecran,spawn)

    def draw(self,ecran,font,dt):
        # Remplit l'écran avec du noir puis dessine le fond
        self.ecran.fill((0,0,0))
        self.ecran.blit(self.background,(0,0))

        # Affiche le joueur
        self.player.draw(self.ecran,font,dt)

        # Récupère la position de la souris
        self.pos = pygame.mouse.get_pos()

        # Affiche diverses informations pour le débogage ou à titre indicatif
        afficher_texte(ecran,font,f"Gravity : {self.player.gravity}",(300,0),"orange")
        afficher_texte(ecran,font,f"Coordinates y : {self.player.joueur.y}",(0,0),"red")
        afficher_texte(ecran,font,f"Coordinates x : {self.player.joueur.x}",(0,20),"black")
        afficher_texte(ecran,font,f'position :{self.pos}',(600,0),'black')


        # Met à jour l'affichage à l'écran
        pygame.display.update()

    def update(self, dt):
        if self.ball:
            self.ball.update(dt)

    def handling(self):
        # Récupère les événements pygame (clavier, souris, fermeture...)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                # Quitte le jeu si on ferme la fenêtre
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Quitte le jeu si on appuie sur Echap
                    self.running = False

            if event.type == pygame.VIDEORESIZE:
                # Met à jour la taille de la fenêtre et redimensionne le fond
                self.ecran = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                self.background = pygame.transform.scale(self.background_original, (event.w, event.h))

        # Délègue les événements clavier au joueur
        self.player.handle_event(events)
        self.arrow.handle_events(self.player.joueur, self.player.spawn,events)

    def run(self):

        # Boucle principale du jeu
        self.creer_arrow(self.player.spawn)  # Crée la flèche une seule fois au début
        while self.running:
            dt = self.clock.tick(60) / 1000  # Delta time en secondes
            self.handling()  # Gère les événements
            # Met à jour la flèche avec le temps écoulé
            self.arrow.update(dt)
            self.draw(self.ecran,self.font,dt)  # Met à jour l'affichage

        # Ferme proprement pygame quand on sort de la boucle
        pygame.quit()
