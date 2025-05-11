import pygame
import math

from src.core.config import *

#
class Arrow:
    def __init__(self, gravity=0.5, color=(0, 0, 0), width=2, length_factor=0.5):
        self.gravity = gravity
        self.color = color
        self.width = width
        self.length_factor = length_factor

    def draw_trajectory(self, surface, start_pos, angle, power, steps=20):
        x = float(start_pos[0])
        y = float(start_pos[1])
        vel_x = math.cos(angle) * power
        vel_y = math.sin(angle) * power
        radius = BALL_RADIUS  # doit être importé depuis config

        for _ in range(steps):
            x += vel_x
            y += vel_y

            if 0 <= x <= surface.get_width() and 0 <= y <= surface.get_height():
                pygame.draw.circle(surface, (200, 0, 200), (int(x), int(y)), 4)
            else:
                break

            vel_y += self.gravity

            if y + radius >= surface.get_height():
                y = surface.get_height() - radius
                if abs(vel_y) > 1:
                    vel_y *= -0.5
                    vel_x *= 0.95
                else:
                    break

            if x - radius <= 0:
                x = radius
                vel_x *= -0.8
            elif x + radius >= surface.get_width():
                x = surface.get_width() - radius
                vel_x *= -0.8