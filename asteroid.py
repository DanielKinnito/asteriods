import pygame
import random
import math

from circleshape import CircleShape
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LINE_WIDTH, ASTEROID_MIN_RADIUS,
    ASTEROID_VERTEX_COUNT, ASTEROID_LUMP_VARIANCE,
    ASTEROID_ROTATION_SPEED_MIN, ASTEROID_ROTATION_SPEED_MAX,
)
from logger import log_event


class Asteroid(CircleShape):
    """
    Asteroid with irregular lumpy shape and rotation.
    Splits into smaller asteroids when destroyed.
    """
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_speed = random.uniform(
            ASTEROID_ROTATION_SPEED_MIN, 
            ASTEROID_ROTATION_SPEED_MAX
        ) * random.choice([-1, 1])  # random direction
        
        # Generate lumpy shape vertices
        self.vertex_offsets = self._generate_shape()
        
        # Color based on size (larger = darker/more brown)
        size_factor = min(1, radius / 60)
        self.color = (
            int(150 + 50 * (1 - size_factor)),  # R
            int(140 + 40 * (1 - size_factor)),  # G  
            int(130 + 30 * (1 - size_factor))   # B
        )
    
    def _generate_shape(self):
        """Generate random vertex offsets for lumpy shape."""
        offsets = []
        for i in range(ASTEROID_VERTEX_COUNT):
            # Random distance from center (with variance)
            distance = self.radius * (1 - ASTEROID_LUMP_VARIANCE / 2 + 
                                      random.uniform(0, ASTEROID_LUMP_VARIANCE))
            offsets.append(distance)
        return offsets
    
    def get_vertices(self):
        """Calculate current vertex positions based on rotation."""
        vertices = []
        for i, offset in enumerate(self.vertex_offsets):
            angle = (360 / ASTEROID_VERTEX_COUNT) * i + self.rotation
            rad = math.radians(angle)
            x = self.position.x + math.cos(rad) * offset
            y = self.position.y + math.sin(rad) * offset
            vertices.append((x, y))
        return vertices
    
    def draw(self, surface):
        """Draw lumpy asteroid polygon with subtle shading."""
        vertices = self.get_vertices()
        
        # Draw shadow/depth (offset slightly)
        shadow_verts = [(v[0] + 2, v[1] + 2) for v in vertices]
        shadow_color = tuple(max(0, c - 50) for c in self.color)
        pygame.draw.polygon(surface, shadow_color, shadow_verts)
        
        # Draw main asteroid body
        pygame.draw.polygon(surface, self.color, vertices)
        
        # Draw outline
        pygame.draw.polygon(surface, (200, 200, 200), vertices, LINE_WIDTH)
        
        # Add some crater details for larger asteroids
        if self.radius > 30:
            self._draw_craters(surface)
    
    def _draw_craters(self, surface):
        """Draw simple crater details on larger asteroids."""
        # Use seed based on position for consistent craters
        random.seed(int(self.vertex_offsets[0] * 1000))
        
        num_craters = int(self.radius / 15)
        for _ in range(num_craters):
            # Random position within asteroid
            angle = random.uniform(0, 360)
            dist = random.uniform(0, self.radius * 0.6)
            rad = math.radians(angle + self.rotation)
            cx = self.position.x + math.cos(rad) * dist
            cy = self.position.y + math.sin(rad) * dist
            
            crater_radius = random.randint(2, int(self.radius / 6))
            crater_color = tuple(max(0, c - 30) for c in self.color)
            pygame.draw.circle(surface, crater_color, (int(cx), int(cy)), crater_radius)
        
        # Reset random seed
        random.seed()
    
    def update(self, dt):
        """Move and rotate asteroid."""
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_screen()
    
    def split(self):
        """
        Split asteroid into smaller pieces.
        Returns position and radius for explosion effect.
        """
        pos_x, pos_y = self.position.x, self.position.y
        radius = self.radius
        
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return (pos_x, pos_y, radius)
        
        log_event("Asteroid split!")
        
        def create_split_asteroid(angle_offset):
            velocity = self.velocity.rotate(angle_offset) * 1.2  # slightly faster
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = velocity
            return asteroid

        angle = random.uniform(20, 50)
        create_split_asteroid(angle)
        create_split_asteroid(-angle)
        
        return (pos_x, pos_y, radius)