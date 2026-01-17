"""
Explosion particle effect system for asteroid destruction.
Creates a burst of colorful particles that fade out over time.
"""
import pygame
import random
import math
from constants import (
    EXPLOSION_PARTICLE_COUNT,
    EXPLOSION_PARTICLE_SPEED_MIN,
    EXPLOSION_PARTICLE_SPEED_MAX,
    EXPLOSION_DURATION,
    EXPLOSION_COLORS,
)


class Particle:
    """Individual explosion particle with physics and fade."""
    
    def __init__(self, x, y, velocity, color, size):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.color = color
        self.size = size
        self.alpha = 255
    
    def update(self, dt, fade_rate):
        """Move particle and reduce alpha."""
        self.position += self.velocity * dt
        self.velocity *= 0.98  # slight drag
        self.alpha = max(0, self.alpha - fade_rate * dt)
        self.size = max(0.5, self.size - dt * 2)
    
    def draw(self, surface):
        """Draw particle with current alpha."""
        if self.alpha <= 0:
            return
        # Create a temporary surface for alpha blending
        r, g, b = self.color
        color_with_alpha = (r, g, b, int(self.alpha))
        size_int = max(1, int(self.size))
        
        # Draw glow effect
        glow_surf = pygame.Surface((size_int * 4, size_int * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf,
            (r, g, b, int(self.alpha * 0.3)),
            (size_int * 2, size_int * 2),
            size_int * 2
        )
        surface.blit(glow_surf, (self.position.x - size_int * 2, self.position.y - size_int * 2))
        
        # Draw core particle
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), size_int)


class Explosion(pygame.sprite.Sprite):
    """
    Explosion effect that spawns at a position and manages particle burst.
    Auto-removes itself when animation completes.
    """
    
    def __init__(self, x, y, radius=30):
        if hasattr(self, 'containers'):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.timer = EXPLOSION_DURATION
        self.fade_rate = 255 / EXPLOSION_DURATION
        
        # Create particles
        self.particles = []
        particle_count = int(EXPLOSION_PARTICLE_COUNT * (radius / 30))  # scale with asteroid size
        
        for _ in range(particle_count):
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(EXPLOSION_PARTICLE_SPEED_MIN, EXPLOSION_PARTICLE_SPEED_MAX)
            speed *= (radius / 30)  # larger asteroids = faster particles
            
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            
            # Color gradient: starts with bright colors, ends with gray
            color = random.choice(EXPLOSION_COLORS[:4])  # exclude gray initially
            size = random.uniform(2, 5)
            
            self.particles.append(Particle(x, y, velocity, color, size))
        
        # Add some smoke particles (gray, slower)
        for _ in range(particle_count // 3):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(EXPLOSION_PARTICLE_SPEED_MIN * 0.5, EXPLOSION_PARTICLE_SPEED_MAX * 0.3)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            color = EXPLOSION_COLORS[4]  # gray smoke
            size = random.uniform(3, 7)
            self.particles.append(Particle(x, y, velocity, color, size))
    
    def update(self, dt):
        """Update all particles and check if explosion is done."""
        self.timer -= dt
        
        for particle in self.particles:
            particle.update(dt, self.fade_rate)
        
        # Remove explosion when timer expires
        if self.timer <= 0:
            self.kill()
    
    def draw(self, surface):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(surface)


def create_explosion(x, y, radius=30):
    """Factory function to create an explosion at position."""
    return Explosion(x, y, radius)
