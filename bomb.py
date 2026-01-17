"""
Bomb system - droppable explosives with delayed detonation.
"""
import pygame
import math
from circleshape import CircleShape
from constants import (
    BOMB_RADIUS,
    BOMB_FUSE_TIME,
    BOMB_EXPLOSION_RADIUS,
    BOMB_COLORS,
    LINE_WIDTH,
)


class Bomb(CircleShape):
    """
    Droppable bomb with fuse timer.
    Blinks faster as it nears detonation, then explodes.
    """
    
    def __init__(self, x, y, velocity):
        super().__init__(x, y, BOMB_RADIUS)
        self.velocity = velocity
        self.fuse_timer = BOMB_FUSE_TIME
        self.blink_phase = 0
        self.exploded = False
    
    @property
    def is_detonating(self):
        """Check if bomb is about to detonate."""
        return self.fuse_timer <= 0.2
    
    def update(self, dt):
        """Update bomb position and fuse timer."""
        # Move with momentum (slowing down)
        self.velocity *= (1 - 0.5 * dt)
        self.position += self.velocity * dt
        
        # Wrap around screen
        self.wrap_screen()
        
        # Count down fuse
        self.fuse_timer -= dt
        
        # Update blink rate (faster as fuse gets shorter)
        blink_speed = 3 + (BOMB_FUSE_TIME - self.fuse_timer) * 5
        self.blink_phase += dt * blink_speed
        
        # Trigger explosion
        if self.fuse_timer <= 0:
            self.exploded = True
    
    def draw(self, surface):
        """Draw bomb with blinking effect."""
        x, y = int(self.position.x), int(self.position.y)
        
        # Blink between two colors
        color_index = int(self.blink_phase) % 2
        color = BOMB_COLORS[color_index]
        
        # Draw bomb body
        pygame.draw.circle(surface, color, (x, y), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), self.radius, LINE_WIDTH)
        
        # Draw fuse indicator (arc that shrinks)
        fuse_angle = (self.fuse_timer / BOMB_FUSE_TIME) * 360
        if fuse_angle > 0:
            rect = pygame.Rect(x - self.radius - 4, y - self.radius - 4, 
                              (self.radius + 4) * 2, (self.radius + 4) * 2)
            pygame.draw.arc(surface, (255, 200, 50), rect, 
                          math.radians(90), math.radians(90 + fuse_angle), 2)
        
        # Warning flash when about to explode
        if self.fuse_timer < 0.5 and int(self.fuse_timer * 8) % 2 == 0:
            pygame.draw.circle(surface, (255, 255, 200), (x, y), self.radius + 5, 2)
    
    def get_blast_radius(self):
        """Get the explosion radius for collision detection."""
        return BOMB_EXPLOSION_RADIUS
    
    def check_asteroid_in_blast(self, asteroid_pos, asteroid_radius):
        """Check if an asteroid is within blast radius."""
        distance = self.position.distance_to(asteroid_pos)
        return distance <= BOMB_EXPLOSION_RADIUS + asteroid_radius


class BombInventory:
    """Manages player's bomb count and dropping."""
    
    def __init__(self, max_bombs=3):
        self.max_bombs = max_bombs
        self.bombs = max_bombs
        self.drop_cooldown = 0
    
    def update(self, dt):
        """Update drop cooldown."""
        if self.drop_cooldown > 0:
            self.drop_cooldown -= dt
    
    def can_drop(self):
        """Check if player can drop a bomb."""
        return self.bombs > 0 and self.drop_cooldown <= 0
    
    def drop(self, position, player_velocity, player_rotation):
        """
        Drop a bomb behind the player.
        Returns Bomb instance or None.
        """
        if not self.can_drop():
            return None
        
        self.bombs -= 1
        self.drop_cooldown = 0.5  # half second between drops
        
        # Calculate backward direction
        backward = pygame.Vector2(0, -1).rotate(player_rotation)
        
        # Bomb inherits some of player velocity plus backward motion
        bomb_velocity = player_velocity * 0.5 + backward * 50
        
        return Bomb(position.x, position.y, bomb_velocity)
    
    def add_bomb(self):
        """Add a bomb to inventory (capped at max)."""
        self.bombs = min(self.bombs + 1, self.max_bombs)
    
    def reset(self):
        """Reset bombs for new life."""
        self.bombs = self.max_bombs
