import math
import pygame

class Ball:
    def __init__(self, x, y, angle, force):
        self.x = x  # Initial horizontal position of the ball
        self.y = y  # Initial vertical position of the ball
        self.radius = 20  # Radius of the ball

        # Calculate initial velocity in x and y based on angle and force
        self.vx = force * math.cos(math.radians(angle)) * 1.2  # Horizontal velocity
        self.vy = -force * math.sin(math.radians(angle)) * 1.2  # Vertical velocity (negative because upwards)
        self.gravity = 0.5  # Gravity applied progressively to vertical velocity

    def update(self):
        # Update the ball's position based on its velocity
        self.x += self.vx
        self.y += self.vy

        # Apply gravity to vertical velocity
        self.vy += self.gravity

    def draw(self, screen):
        # Render the ball on the screen
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.radius)
