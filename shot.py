import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS


class Shot(CircleShape):
    """
    Projectile fired by player.
    Supports different weapon types with varying colors, sizes, and damage.
    """
    
    def __init__(self, x, y, radius=SHOT_RADIUS, color=(255, 255, 100), damage=1):
        super().__init__(x, y, radius)
        self.color = color
        self.damage = damage
        self.lifetime = 3.0  # despawn after 3 seconds
    
    def draw(self, surface):
        """Draw shot with glow effect based on weapon type."""
        x, y = int(self.position.x), int(self.position.y)
        
        # Outer glow
        glow_color = tuple(max(0, c - 100) for c in self.color)
        if self.radius > 2:
            pygame.draw.circle(surface, glow_color, (x, y), self.radius + 2)
        
        # Core
        pygame.draw.circle(surface, self.color, (x, y), max(1, int(self.radius)))
        
        # Bright center
        if self.radius >= 3:
            center_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(surface, center_color, (x, y), max(1, int(self.radius) - 1))
    
    def update(self, dt):
        """Move shot and wrap around screen."""
        self.position += self.velocity * dt
        self.wrap_screen()
        
        # Reduce lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()