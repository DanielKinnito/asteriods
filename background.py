"""
Parallax starfield background with multiple layers.
Creates a sense of depth and movement in space.
"""
import pygame
import random
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STAR_LAYERS,
    STARS_PER_LAYER,
    STAR_SPEEDS,
    STAR_SIZES,
    STAR_COLORS,
)


class Star:
    """Individual star with twinkle effect."""
    
    def __init__(self, x, y, layer):
        self.position = pygame.Vector2(x, y)
        self.layer = layer
        self.base_brightness = random.uniform(0.6, 1.0)
        self.twinkle_speed = random.uniform(1.5, 4.0)
        self.twinkle_phase = random.uniform(0, 6.28)  # random start phase
        self.size = STAR_SIZES[layer]
    
    def get_brightness(self, time):
        """Calculate current brightness with twinkle effect."""
        import math
        twinkle = 0.5 + 0.5 * math.sin(self.twinkle_phase + time * self.twinkle_speed)
        return self.base_brightness * (0.7 + 0.3 * twinkle)
    
    def update_parallax(self, camera_delta, layer_speed):
        """Move star based on parallax layer speed."""
        self.position.x -= camera_delta.x * layer_speed
        self.position.y -= camera_delta.y * layer_speed
        
        # Wrap around screen
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH
        
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT


class Background:
    """
    Multi-layer parallax starfield background.
    Layers further away move slower, creating depth illusion.
    """
    
    def __init__(self):
        self.stars = []
        self.time = 0
        self.last_player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Create stars for each layer
        for layer in range(STAR_LAYERS):
            for _ in range(STARS_PER_LAYER[layer]):
                x = random.uniform(0, SCREEN_WIDTH)
                y = random.uniform(0, SCREEN_HEIGHT)
                self.stars.append(Star(x, y, layer))
        
        # Create gradient background surface (dark blue to black)
        self.gradient_surface = self._create_gradient()
    
    def _create_gradient(self):
        """Create a subtle space nebula gradient."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Base: very dark with subtle blue tint
        for y in range(SCREEN_HEIGHT):
            # Gradient from dark purple-blue at top to pure black at bottom
            progress = y / SCREEN_HEIGHT
            r = int(5 * (1 - progress))
            g = int(5 * (1 - progress))
            b = int(15 * (1 - progress))
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Add some nebula spots
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(100, 300)
            
            # Choose nebula color
            colors = [(20, 10, 30), (10, 15, 25), (15, 5, 20)]
            color = random.choice(colors)
            
            # Draw soft nebula
            for r in range(radius, 0, -10):
                alpha = int(10 * (r / radius))
                nebula_color = tuple(min(255, c + alpha) for c in color)
                pygame.draw.circle(surface, nebula_color, (x, y), r)
        
        return surface
    
    def update(self, dt, player_pos=None):
        """Update starfield with parallax based on player movement."""
        self.time += dt
        
        if player_pos is not None:
            # Calculate camera movement delta
            delta = player_pos - self.last_player_pos
            self.last_player_pos = pygame.Vector2(player_pos)
            
            # Update each star with parallax
            for star in self.stars:
                star.update_parallax(delta, STAR_SPEEDS[star.layer])
    
    def draw(self, surface):
        """Draw gradient background and all stars."""
        # Draw gradient first
        surface.blit(self.gradient_surface, (0, 0))
        
        # Draw stars by layer (far to near)
        for star in self.stars:
            brightness = star.get_brightness(self.time)
            base_color = STAR_COLORS[star.layer]
            color = tuple(int(c * brightness) for c in base_color)
            
            pos = (int(star.position.x), int(star.position.y))
            
            if star.size == 1:
                surface.set_at(pos, color)
            else:
                pygame.draw.circle(surface, color, pos, star.size)
                
                # Add subtle glow for larger stars
                if star.size >= 2 and brightness > 0.8:
                    glow_color = tuple(int(c * 0.3) for c in color)
                    pygame.draw.circle(surface, glow_color, pos, star.size + 1)
