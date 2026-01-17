import pygame
import random

from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()


    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("Asteroid split!")
            def create_split_asteroid(angle_offset):
                velocity = self.velocity.rotate(angle_offset)
                new_radius = self.radius - ASTEROID_MIN_RADIUS
                asteroid = Asteroid(self.position.x, self.position.y, new_radius)
                asteroid.velocity = velocity
                return asteroid

            angle = random.uniform(20, 50)
            asteroid1 = create_split_asteroid(angle)
            asteroid2 = create_split_asteroid(-angle)