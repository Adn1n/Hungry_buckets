import pygame
import math

class Arrow:
    def __init__(self, base_color=(255, 0, 0), width=2, length_factor=10.0):
        self.base_color = base_color
        self.width = width
        self.length_factor = length_factor

    def draw(self, surface, player_pos, start_pos, current_pos,mouse_pos):
        dx = start_pos[0] - mouse_pos[0]
        dy = start_pos[1] - mouse_pos[1]

        # Calcul angle + puissance
        angle = math.atan2(-dy, -dx)
        distance = math.hypot(dx, dy)
        power = min(distance / 4, 20)

        # Simulation du tir
        gravity = 0.5
        vel_x = math.cos(angle) * power
        vel_y = math.sin(angle) * power

        # Points de la trajectoire
        num_points = int(30 * (power / 20) * self.length_factor)
        num_points = max(5, min(60, num_points))
        time_step = 0.1
        points = []
        for i in range(1, num_points + 1):
            t = i * time_step
            x = player_pos[0] + vel_x * t
            y = player_pos[1] + vel_y * t + 0.5 * gravity * t * t
            points.append((x, y))

        # Couleur dynamique selon puissance
        r = min(255, int((power / 20) * 255))
        g = 255 - r
        color = (r, g, 0)


        # Flèche principale en pointillés (plus fine)
        for i in range(0, len(points) - 1, 2):
            pygame.draw.line(surface, color, points[i], points[i + 1], max(1, self.width))

        # Tête de flèche triangulaire agrandie
        if len(points) >= 2:
            angle = math.atan2(points[-1][1] - points[-2][1], points[-1][0] - points[-2][0])
            head_len = 20
            end_pos = points[-1]
            left = (
                end_pos[0] - head_len * math.cos(angle - 0.5),
                end_pos[1] - head_len * math.sin(angle - 0.5),
            )
            right = (
                end_pos[0] - head_len * math.cos(angle + 0.5),
                end_pos[1] - head_len * math.sin(angle + 0.5),
            )
            pygame.draw.polygon(surface, color, [end_pos, left, right])
