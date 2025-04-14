import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Joueur au centre
player_pos = pygame.Rect(400, 300, 40, 40)
angle = 45
force = 10
angle_offset_deg = 30  # ouverture du triangle de la flèche

def draw_arrow(screen, player_center, angle, force):
    arrow_length = 20 + force * 3
    rad = math.radians(angle)
    x_end = player_center[0] + arrow_length * math.cos(rad)
    y_end = player_center[1] - arrow_length * math.sin(rad)

    pygame.draw.line(screen, (0, 255, 0), player_center, (x_end, y_end), 7)

    # flèche triangle
    angle_offset = math.radians(angle_offset_deg)
    side = 20

    left_x = x_end - side * math.cos(rad - angle_offset)
    left_y = y_end + side * math.sin(rad - angle_offset)

    right_x = x_end - side * math.cos(rad + angle_offset)
    right_y = y_end + side * math.sin(rad + angle_offset)

    pygame.draw.polygon(screen, (0, 255, 0), [(x_end, y_end), (left_x, left_y), (right_x, right_y)])

def draw_text(surface, text, x, y):
    img = font.render(text, True, (255, 255, 255))
    surface.blit(img, (x, y))

running = True
while running:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        angle = max(0, angle - 5)
    if keys[pygame.K_LEFT]:
        angle = min(180, angle + 5)
    if keys[pygame.K_UP]:
        force += 1
    if keys[pygame.K_DOWN]:
        force = max(1, force - 1)
    if keys[pygame.K_a]:
        angle_offset_deg = max(5, angle_offset_deg - 1)
    if keys[pygame.K_e]:
        angle_offset_deg = min(80, angle_offset_deg + 1)

    pygame.draw.rect(screen, (0, 120, 255), player_pos)
    draw_arrow(screen, player_pos.center, angle, force)
    draw_text(screen, f"Angle: {angle}°", 10, 10)
    draw_text(screen, f"Force: {force}", 10, 40)
    draw_text(screen, f"Angle Offset: {angle_offset_deg}°", 10, 70)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
