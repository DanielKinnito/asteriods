"""
Weapon system with multiple weapon types.
Each weapon defines fire rate, projectile behavior, and visual style.
"""
import pygame
from constants import (
    WEAPON_STANDARD,
    WEAPON_SPREAD,
    WEAPON_RAPID,
    WEAPON_LASER,
    WEAPON_CONFIGS,
    SHOT_RADIUS,
)
from shot import Shot


class Weapon:
    """Base weapon class with firing behavior."""
    
    def __init__(self, weapon_type=WEAPON_STANDARD):
        self.weapon_type = weapon_type
        self.config = WEAPON_CONFIGS[weapon_type]
        self.cooldown_timer = 0
    
    @property
    def name(self):
        return self.config["name"]
    
    @property
    def cooldown(self):
        return self.config["cooldown"]
    
    @property
    def shot_speed(self):
        return self.config["shot_speed"]
    
    @property
    def shot_count(self):
        return self.config["shot_count"]
    
    @property
    def spread_angle(self):
        return self.config["spread_angle"]
    
    @property
    def color(self):
        return self.config["color"]
    
    @property
    def damage(self):
        return self.config["damage"]
    
    def update(self, dt):
        """Update cooldown timer."""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
    
    def can_fire(self):
        """Check if weapon is ready to fire."""
        return self.cooldown_timer <= 0
    
    def fire(self, position, rotation):
        """
        Fire the weapon, creating projectiles.
        Returns list of Shot objects.
        """
        if not self.can_fire():
            return []
        
        self.cooldown_timer = self.cooldown
        shots = []
        
        # Calculate base direction
        forward = pygame.Vector2(0, 1).rotate(rotation)
        
        # Create shots based on weapon type
        if self.shot_count == 1:
            # Single shot
            shot = self._create_shot(position, forward)
            shots.append(shot)
        else:
            # Multiple shots in a spread pattern
            total_spread = self.spread_angle * (self.shot_count - 1)
            start_angle = -total_spread / 2
            
            for i in range(self.shot_count):
                angle_offset = start_angle + (self.spread_angle * i)
                direction = forward.rotate(angle_offset)
                shot = self._create_shot(position, direction)
                shots.append(shot)
        
        return shots
    
    def _create_shot(self, position, direction):
        """Create a single shot projectile."""
        size = self.config.get("size", SHOT_RADIUS)
        shot = Shot(position.x, position.y, size, self.color, self.damage)
        shot.velocity = direction * self.shot_speed
        return shot


class WeaponManager:
    """Manages player's weapon inventory and switching."""
    
    def __init__(self):
        self.available_weapons = [WEAPON_STANDARD]  # Start with standard only
        self.current_index = 0
        self.weapons = {
            WEAPON_STANDARD: Weapon(WEAPON_STANDARD),
            WEAPON_SPREAD: Weapon(WEAPON_SPREAD),
            WEAPON_RAPID: Weapon(WEAPON_RAPID),
            WEAPON_LASER: Weapon(WEAPON_LASER),
        }
        self.temp_weapon = None  # Temporary weapon from power-up
        self.temp_weapon_timer = 0
    
    @property
    def current_weapon(self):
        """Get the currently active weapon."""
        if self.temp_weapon is not None:
            return self.temp_weapon
        weapon_type = self.available_weapons[self.current_index]
        return self.weapons[weapon_type]
    
    def update(self, dt):
        """Update all weapons and temporary weapon timer."""
        for weapon in self.weapons.values():
            weapon.update(dt)
        
        if self.temp_weapon_timer > 0:
            self.temp_weapon_timer -= dt
            if self.temp_weapon_timer <= 0:
                self.temp_weapon = None
    
    def switch_weapon(self, index):
        """Switch to weapon at index (0-based, within available weapons)."""
        if 0 <= index < len(self.available_weapons):
            self.current_index = index
            return True
        return False
    
    def cycle_weapon(self, direction=1):
        """Cycle through available weapons."""
        if len(self.available_weapons) > 1:
            self.current_index = (self.current_index + direction) % len(self.available_weapons)
    
    def unlock_weapon(self, weapon_type):
        """Add a weapon to available inventory."""
        if weapon_type not in self.available_weapons:
            self.available_weapons.append(weapon_type)
    
    def set_temporary_weapon(self, weapon_type, duration):
        """Set a temporary weapon (from power-up)."""
        self.temp_weapon = self.weapons[weapon_type]
        self.temp_weapon_timer = duration
    
    def fire(self, position, rotation):
        """Fire current weapon."""
        return self.current_weapon.fire(position, rotation)
    
    def can_fire(self):
        """Check if current weapon can fire."""
        return self.current_weapon.can_fire()
