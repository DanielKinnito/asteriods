"""
Power-up system with collectible items and timed effects.
"""
import pygame
import random
import math
from circleshape import CircleShape
from constants import (
    POWERUP_RADIUS,
    POWERUP_FLOAT_SPEED,
    POWERUP_FLOAT_AMPLITUDE,
    POWERUP_SHIELD,
    POWERUP_SPEED,
    POWERUP_WEAPON,
    POWERUP_CONFIGS,
    POWERUP_SPAWN_CHANCE,
    LINE_WIDTH,
)


class PowerUp(CircleShape):
    """
    Collectible power-up that grants temporary abilities.
    Floats with a bobbing animation and has a glowing effect.
    """
    
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, POWERUP_RADIUS)
        self.powerup_type = powerup_type
        self.config = POWERUP_CONFIGS[powerup_type]
        self.time = random.uniform(0, 6.28)  # random phase
        self.base_y = y
        self.glow_phase = 0
        self.lifetime = 15.0  # despawn after 15 seconds
    
    @property
    def color(self):
        return self.config["color"]
    
    @property
    def duration(self):
        return self.config["duration"]
    
    @property
    def icon(self):
        return self.config["icon"]
    
    @property
    def name(self):
        return self.config["name"]
    
    def update(self, dt):
        """Update floating animation and lifetime."""
        self.time += dt * POWERUP_FLOAT_SPEED
        self.glow_phase += dt * 4
        
        # Bobbing effect
        self.position.y = self.base_y + math.sin(self.time) * POWERUP_FLOAT_AMPLITUDE
        
        # Apply any velocity (for drifting)
        self.position += self.velocity * dt
        self.base_y += self.velocity.y * dt
        
        # Wrap around screen
        self.wrap_screen()
        
        # Reduce lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
    
    def draw(self, surface):
        """Draw power-up with glow effect."""
        x, y = int(self.position.x), int(self.position.y)
        
        # Pulsing glow
        glow_intensity = 0.5 + 0.5 * math.sin(self.glow_phase)
        glow_radius = int(self.radius + 8 * glow_intensity)
        
        # Outer glow
        glow_color = tuple(int(c * 0.3 * glow_intensity) for c in self.color)
        pygame.draw.circle(surface, glow_color, (x, y), glow_radius)
        
        # Middle ring
        pygame.draw.circle(surface, self.color, (x, y), self.radius, LINE_WIDTH)
        
        # Inner fill (semi-transparent effect via darker color)
        inner_color = tuple(c // 3 for c in self.color)
        pygame.draw.circle(surface, inner_color, (x, y), self.radius - LINE_WIDTH)
        
        # Draw icon
        font = pygame.font.Font(None, 24)
        text = font.render(self.icon, True, self.color)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
        
        # Blinking when about to expire
        if self.lifetime < 3 and int(self.lifetime * 4) % 2 == 0:
            pygame.draw.circle(surface, (255, 255, 255), (x, y), self.radius + 2, 1)


class PowerUpManager:
    """Manages active power-up effects on the player."""
    
    def __init__(self):
        self.active_effects = {}  # {powerup_type: remaining_duration}
    
    def apply(self, powerup_type, duration):
        """Apply or refresh a power-up effect."""
        self.active_effects[powerup_type] = duration
    
    def update(self, dt):
        """Update all active effect timers."""
        expired = []
        for powerup_type in self.active_effects:
            self.active_effects[powerup_type] -= dt
            if self.active_effects[powerup_type] <= 0:
                expired.append(powerup_type)
        
        for powerup_type in expired:
            del self.active_effects[powerup_type]
    
    def is_active(self, powerup_type):
        """Check if a power-up effect is active."""
        return powerup_type in self.active_effects
    
    def get_remaining(self, powerup_type):
        """Get remaining duration of an effect."""
        return self.active_effects.get(powerup_type, 0)
    
    def has_shield(self):
        """Check if shield is active."""
        return self.is_active(POWERUP_SHIELD)
    
    def has_speed_boost(self):
        """Check if speed boost is active."""
        return self.is_active(POWERUP_SPEED)


def maybe_spawn_powerup(x, y):
    """
    Randomly spawn a power-up at the given position.
    Returns PowerUp instance or None.
    """
    if random.random() > POWERUP_SPAWN_CHANCE:
        return None
    
    # Weight towards shield and speed, weapon is rarer
    weights = [0.4, 0.4, 0.2]  # shield, speed, weapon
    r = random.random()
    
    if r < weights[0]:
        powerup_type = POWERUP_SHIELD
    elif r < weights[0] + weights[1]:
        powerup_type = POWERUP_SPEED
    else:
        powerup_type = POWERUP_WEAPON
    
    powerup = PowerUp(x, y, powerup_type)
    # Give it a slow random drift
    powerup.velocity = pygame.Vector2(
        random.uniform(-20, 20),
        random.uniform(-20, 20)
    )
    return powerup
