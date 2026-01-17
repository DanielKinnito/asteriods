import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_ACCELERATION, PLAYER_FRICTION
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # in degrees
        self.cooldown_timer = 0
        self.invulnerable_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.invulnerable_timer > 0:
            # Flash or just don't draw every frame, or draw different color
             if int(self.invulnerable_timer * 10) % 2 == 0:
                 return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.cooldown_timer > 0:
                pass
            else:
                self.shoot()
                self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        self.position += self.velocity * dt
        self.wrap_screen()

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

