"""
Player ship class with triangular hitbox, weapon system, and power-ups.
"""
import pygame
import math
from circleshape import CircleShape, polygon_collides_circle
from constants import (
    PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED,
    PLAYER_ACCELERATION, PLAYER_FRICTION, PLAYER_ACCELERATION_BOOST,
    SHIELD_RING_RADIUS, WEAPON_STANDARD, WEAPON_SPREAD, WEAPON_RAPID, WEAPON_LASER,
    SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPEED,
)
from weapons import WeaponManager
from bomb import BombInventory
from powerup import PowerUpManager


class Player(CircleShape):
    """
    Player spaceship with triangular shape and physics-based movement.
    Features weapon system, bombs, and power-up effects.
    """
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # in degrees
        self.invulnerable_timer = 0
        
        # Systems
        self.weapon_manager = WeaponManager()
        self.bomb_inventory = BombInventory()
        self.powerup_manager = PowerUpManager()
        
        # Engine effect
        self.is_thrusting = False
        self.thrust_flicker = 0
    
    def triangle(self):
        """Calculate triangle vertices for rendering and collision."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def collides_with(self, other):
        """
        Check collision using triangular hitbox.
        Uses polygon-circle collision for accurate detection.
        """
        tri_verts = self.triangle()
        # Convert to tuples for collision function
        tri_tuples = [(v.x, v.y) for v in tri_verts]
        return polygon_collides_circle(tri_tuples, other.position, other.radius)
    
    def draw(self, screen):
        """Draw player ship with effects."""
        # Handle invulnerability flashing
        if self.invulnerable_timer > 0:
            if int(self.invulnerable_timer * 10) % 2 == 0:
                return
        
        tri = self.triangle()
        
        # Draw engine exhaust if thrusting
        if self.is_thrusting:
            self._draw_exhaust(screen, tri)
        
        # Draw shield if active
        if self.powerup_manager.has_shield():
            self._draw_shield(screen)
        
        # Draw ship body
        # Ship color (with speed boost glow)
        if self.powerup_manager.has_speed_boost():
            ship_color = (255, 220, 100)  # golden glow
        else:
            ship_color = (255, 255, 255)
        
        # Draw ship shadow
        shadow_tri = [(v.x + 2, v.y + 2) for v in tri]
        pygame.draw.polygon(screen, (30, 30, 40), shadow_tri)
        
        # Draw ship fill
        pygame.draw.polygon(screen, (40, 50, 60), [(v.x, v.y) for v in tri])
        
        # Draw ship outline
        pygame.draw.polygon(screen, ship_color, [(v.x, v.y) for v in tri], LINE_WIDTH)
        
        # Draw cockpit
        cockpit_pos = self.position + pygame.Vector2(0, 1).rotate(self.rotation) * (self.radius * 0.3)
        pygame.draw.circle(screen, (100, 150, 255), (int(cockpit_pos.x), int(cockpit_pos.y)), 4)
    
    def _draw_exhaust(self, screen, tri):
        """Draw engine exhaust flames."""
        self.thrust_flicker += 0.3
        flicker = 0.7 + 0.3 * math.sin(self.thrust_flicker * 10)
        
        backward = pygame.Vector2(0, -1).rotate(self.rotation)
        
        # Calculate exhaust position (back of ship)
        exhaust_base = self.position - pygame.Vector2(0, 1).rotate(self.rotation) * self.radius
        
        # Exhaust flame
        flame_length = 15 * flicker
        if self.powerup_manager.has_speed_boost():
            flame_length *= 1.5
            flame_color = (255, 200, 50)
        else:
            flame_color = (255, 150, 50)
        
        flame_tip = exhaust_base + backward * flame_length
        
        # Draw flame triangle
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * 5
        flame_verts = [
            (exhaust_base.x - right.x, exhaust_base.y - right.y),
            (exhaust_base.x + right.x, exhaust_base.y + right.y),
            (flame_tip.x, flame_tip.y)
        ]
        pygame.draw.polygon(screen, flame_color, flame_verts)
        
        # Inner white core
        inner_tip = exhaust_base + backward * (flame_length * 0.5)
        inner_verts = [
            (exhaust_base.x - right.x * 0.5, exhaust_base.y - right.y * 0.5),
            (exhaust_base.x + right.x * 0.5, exhaust_base.y + right.y * 0.5),
            (inner_tip.x, inner_tip.y)
        ]
        pygame.draw.polygon(screen, (255, 255, 200), inner_verts)
    
    def _draw_shield(self, screen):
        """Draw shield bubble effect."""
        shield_time = self.powerup_manager.get_remaining(0)  # POWERUP_SHIELD = 0
        
        # Pulsing effect
        pulse = 0.8 + 0.2 * math.sin(shield_time * 5)
        radius = int(SHIELD_RING_RADIUS * pulse)
        
        # Outer glow
        glow_surf = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (100, 150, 255, 50), (radius + 10, radius + 10), radius + 5)
        screen.blit(glow_surf, (self.position.x - radius - 10, self.position.y - radius - 10))
        
        # Shield ring
        alpha = int(150 * pulse)
        if shield_time < 2 and int(shield_time * 4) % 2 == 0:
            # Flicker when about to expire
            alpha = 50
        pygame.draw.circle(screen, (100, 150, 255), 
                          (int(self.position.x), int(self.position.y)), 
                          radius, 2)
    
    def move(self, dt, direction=1):
        """Apply acceleration in facing direction."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        accel = PLAYER_ACCELERATION
        
        # Speed boost multiplier
        if self.powerup_manager.has_speed_boost():
            accel = PLAYER_ACCELERATION_BOOST
        
        self.velocity += forward * accel * dt * direction
    
    def update(self, dt):
        """Update player state, handle input."""
        keys = pygame.key.get_pressed()
        
        # Rotation
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotation += PLAYER_TURN_SPEED * dt
        
        # Thrust
        self.is_thrusting = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
            self.is_thrusting = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt, -0.5)  # weaker reverse thrust
        
        # Update systems
        self.weapon_manager.update(dt)
        self.bomb_inventory.update(dt)
        self.powerup_manager.update(dt)
        
        # Cooldown timers
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        
        # Apply friction and move
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        self.position += self.velocity * dt
        self.wrap_screen()
    
    def shoot(self):
        """Fire current weapon. Returns list of shot objects."""
        return self.weapon_manager.fire(self.position.copy(), self.rotation)
    
    def drop_bomb(self):
        """Drop a bomb. Returns Bomb object or None."""
        return self.bomb_inventory.drop(
            self.position.copy(), 
            self.velocity.copy(), 
            self.rotation
        )
    
    def switch_weapon(self, weapon_index):
        """Switch to weapon by index (0-3)."""
        # Map index to weapon type
        weapon_types = [WEAPON_STANDARD, WEAPON_SPREAD, WEAPON_RAPID, WEAPON_LASER]
        if 0 <= weapon_index < len(weapon_types):
            weapon_type = weapon_types[weapon_index]
            # Unlock and switch
            self.weapon_manager.unlock_weapon(weapon_type)
            # Find index in available weapons
            if weapon_type in self.weapon_manager.available_weapons:
                idx = self.weapon_manager.available_weapons.index(weapon_type)
                self.weapon_manager.switch_weapon(idx)
    
    def apply_powerup(self, powerup):
        """Apply a collected power-up effect."""
        self.powerup_manager.apply(powerup.powerup_type, powerup.duration)
        
        # Special handling for weapon power-up
        from constants import POWERUP_WEAPON
        if powerup.powerup_type == POWERUP_WEAPON:
            # Grant a random better weapon temporarily
            import random
            weapon_type = random.choice([WEAPON_SPREAD, WEAPON_RAPID, WEAPON_LASER])
            self.weapon_manager.set_temporary_weapon(weapon_type, powerup.duration)
    
    def is_shielded(self):
        """Check if player has active shield."""
        return self.powerup_manager.has_shield()
    
    def reset(self, x, y):
        """Reset player to starting position."""
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = 3
        self.bomb_inventory.reset()
