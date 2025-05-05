import pygame
import math

#
class Arrow:
    def __init__(self, gravity=0.5, color=(0, 0, 0), width=2, length_factor=0.5):
        self.gravity = gravity
        self.color = color
        self.width = width
        self.length_factor = length_factor

    def draw(self, surface, player_pos, start_pos, mouse_pos):
        dx = start_pos[0] - mouse_pos[0]
        dy = start_pos[1] - mouse_pos[1]

        angle = math.atan2(dy, dx)
        distance = math.hypot(dx, dy)
        power = min(distance / 4, 20)

        vel_x = math.cos(angle) * power
        vel_y = math.sin(angle) * power

        num_points = int(30 * (power / 20) * self.length_factor)
        num_points = max(5, min(60, num_points))
        time_interval = 0.05 + (power / 30)

        for i in range(1, num_points + 1):
            t = i * time_interval
            dx = vel_x * t
            dy = vel_y * t + 0.5 * self.gravity * t * t
            point_x = player_pos[0] + dx
            point_y = player_pos[1] + dy
            if 0 < point_x < surface.get_width() and 0 < point_y < surface.get_height():
                pygame.draw.circle(surface, self.color, (int(point_x), int(point_y)), 4)