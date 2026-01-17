"""
Asteroids - Enhanced Edition
A classic arcade game with modern features.
"""
import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    WEAPON_STANDARD, WEAPON_SPREAD, WEAPON_RAPID, WEAPON_LASER,
    POWERUP_SHIELD, POWERUP_SPEED, POWERUP_WEAPON,
    BOMB_EXPLOSION_RADIUS,
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion, create_explosion
from background import Background
from powerup import PowerUp, maybe_spawn_powerup
from bomb import Bomb


def draw_text_centered(screen, font, text, y_offset, color="white"):
    """Draw centered text on screen."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(surface, rect)


def draw_hud(screen, font, score, lives, player):
    """Draw the game HUD with score, lives, weapon, and power-ups."""
    y = 10
    
    # Score
    score_surface = font.render(f"Score: {score}", True, "white")
    screen.blit(score_surface, (10, y))
    
    # Lives (draw ship icons)
    lives_text = font.render("Lives:", True, "white")
    screen.blit(lives_text, (10, y + 30))
    for i in range(lives):
        # Mini ship triangle
        x = 80 + i * 25
        points = [(x, y + 35), (x - 8, y + 50), (x + 8, y + 50)]
        pygame.draw.polygon(screen, "white", points, 2)
    
    # Current weapon (right side)
    weapon_name = player.weapon_manager.current_weapon.name
    weapon_color = player.weapon_manager.current_weapon.color
    weapon_text = font.render(f"Weapon: {weapon_name}", True, weapon_color)
    screen.blit(weapon_text, (SCREEN_WIDTH - 200, y))
    
    # Bombs (right side)
    bombs_left = player.bomb_inventory.bombs
    bombs_text = font.render(f"Bombs: {bombs_left}", True, (255, 100, 100))
    screen.blit(bombs_text, (SCREEN_WIDTH - 200, y + 30))
    
    # Active power-ups
    powerup_y = y + 60
    if player.powerup_manager.has_shield():
        remaining = player.powerup_manager.get_remaining(POWERUP_SHIELD)
        shield_text = font.render(f"SHIELD {remaining:.1f}s", True, (100, 150, 255))
        screen.blit(shield_text, (SCREEN_WIDTH - 200, powerup_y))
        powerup_y += 25
    
    if player.powerup_manager.has_speed_boost():
        remaining = player.powerup_manager.get_remaining(POWERUP_SPEED)
        speed_text = font.render(f"SPEED {remaining:.1f}s", True, (255, 200, 50))
        screen.blit(speed_text, (SCREEN_WIDTH - 200, powerup_y))
    
    # Weapon switch hint (bottom)
    hint_font = pygame.font.Font(None, 24)
    hint_text = hint_font.render("1-4: Switch Weapons | B: Drop Bomb | WASD: Move | SPACE: Shoot", True, (100, 100, 100))
    screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 25))


def main():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids Game with Pygame version:", pygame.__version__)
    print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Enhanced Edition")

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    # Set static containers for auto-grouping
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)

    # Create background (not in groups, drawn first)
    background = Background()

    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 72)
    game_state = "menu"  # menu, playing, game_over
    player = None
    asteroid_field = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if game_state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = "playing"
                    score = 0
                    lives = 3
                    
                    # Reset all groups
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    explosions.empty()
                    powerups.empty()
                    bombs.empty()
                    
                    # Create game objects
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroid_field = AsteroidField()

            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    # Shooting
                    if event.key == pygame.K_SPACE:
                        new_shots = player.shoot()
                        # Shots are auto-added via containers
                    
                    # Weapon switching (1-4 keys)
                    if event.key == pygame.K_1:
                        player.switch_weapon(0)
                    elif event.key == pygame.K_2:
                        player.switch_weapon(1)
                    elif event.key == pygame.K_3:
                        player.switch_weapon(2)
                    elif event.key == pygame.K_4:
                        player.switch_weapon(3)
                    
                    # Bomb dropping
                    if event.key == pygame.K_b:
                        bomb = player.drop_bomb()
                        # Bomb is auto-added via containers

            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_state = "menu"

        # Update background with player position for parallax
        if player:
            background.update(dt, player.position)
        else:
            background.update(dt)
        
        # Draw background first
        background.draw(screen)

        if game_state == "menu":
            # Menu screen
            draw_text_centered(screen, title_font, "ASTEROIDS", -80, (100, 200, 255))
            draw_text_centered(screen, font, "Enhanced Edition", -30, (150, 150, 150))
            draw_text_centered(screen, font, "Press ENTER to Start", 50)
            
            # Feature list
            small_font = pygame.font.Font(None, 24)
            features = [
                "• Multiple weapon types (1-4 to switch)",
                "• Collectible power-ups",
                "• Droppable bombs (B key)",
                "• Physics-based movement"
            ]
            for i, feature in enumerate(features):
                text = small_font.render(feature, True, (120, 120, 120))
                screen.blit(text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100 + i * 25))
        
        elif game_state == "playing":
            # Update all game objects
            updatable.update(dt)

            # Check bomb explosions
            for bomb in list(bombs):
                if bomb.exploded:
                    # Create explosion
                    explosion = create_explosion(bomb.position.x, bomb.position.y, 
                                                 BOMB_EXPLOSION_RADIUS // 2)
                    explosions.add(explosion)
                    log_event("Bomb exploded!")
                    
                    # Destroy asteroids in blast radius
                    for asteroid in list(asteroids):
                        if bomb.check_asteroid_in_blast(asteroid.position, asteroid.radius):
                            pos_x, pos_y, radius = asteroid.split()
                            score += 15  # Bonus for bomb kills
                            # Create smaller explosion for each asteroid
                            exp = create_explosion(pos_x, pos_y, radius)
                            explosions.add(exp)
                    
                    bomb.kill()

            # Player-asteroid collision
            for asteroid in list(asteroids):
                if player.is_shielded():
                    # Shield destroys asteroids on contact
                    if player.collides_with(asteroid):
                        pos_x, pos_y, radius = asteroid.split()
                        explosion = create_explosion(pos_x, pos_y, radius)
                        explosions.add(explosion)
                        score += 5
                        log_event("Shield destroyed asteroid!")
                elif player.invulnerable_timer <= 0 and player.collides_with(asteroid):
                    log_event("Player hit!")
                    lives -= 1
                    
                    # Create explosion at player
                    explosion = create_explosion(player.position.x, player.position.y, 20)
                    explosions.add(explosion)
                    
                    if lives <= 0:
                        game_state = "game_over"
                    else:
                        player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            
            # Shot-asteroid collision
            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        log_event("Asteroid hit!")
                        pos_x, pos_y, radius = asteroid.split()
                        score += 10
                        shot.kill()
                        
                        # Create explosion
                        explosion = create_explosion(pos_x, pos_y, radius)
                        explosions.add(explosion)
                        
                        # Maybe spawn power-up
                        powerup = maybe_spawn_powerup(pos_x, pos_y)
                        if powerup:
                            powerups.add(powerup)
            
            # Player-powerup collision
            for powerup in list(powerups):
                if player.collides_with(powerup):
                    log_event(f"Collected {powerup.name} power-up!")
                    player.apply_powerup(powerup)
                    powerup.kill()
                    score += 25  # Bonus for collecting power-ups

            # Draw all objects (in order: asteroids, shots, player, explosions, powerups)
            for obj in drawable:
                obj.draw(screen)
            
            # Draw HUD
            draw_hud(screen, font, score, lives, player)
            
            log_state()

        elif game_state == "game_over":
            # Keep drawing explosions during game over
            for explosion in explosions:
                explosion.update(dt)
                explosion.draw(screen)
            
            draw_text_centered(screen, title_font, "GAME OVER", -60, (255, 80, 80))
            draw_text_centered(screen, font, f"Final Score: {score}", 0)
            draw_text_centered(screen, font, "Press R to Restart", 60)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
