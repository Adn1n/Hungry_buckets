import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Joueur
player = pygame.Rect(400, 500, 50, 50)
sol_y = player.y
gravity = 0
is_jumping = False
jump_velocity = 15

running = True
while running:
    screen.fill("white")

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not is_jumping:
                is_jumping = True
                gravity = -jump_velocity

    # Logique du saut
    if is_jumping:
        player.y += gravity
        gravity += 1  # effet de gravité

        if player.y >= sol_y:
            player.y = sol_y
            is_jumping = False
            gravity = 0

    # Affichage
    pygame.draw.rect(screen, (3, 255, 255), player)

    # Texte d'infos
    font = pygame.font.SysFont(None, 36)
    text1 = font.render(f"Y : {player.y}", True, "red")
    text2 = font.render(f"Gravity : {gravity}", True, "orange")
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()