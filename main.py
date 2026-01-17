import sys
import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

import sys
import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def draw_text_centered(screen, font, text, y_offset):
    surface = font.render(text, True, "white")
    rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(surface, rect)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids Game with Pygame version:", pygame.__version__)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set static containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    game_state = "menu" # menu, playing, game_over
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
                    
                    # Reset groups
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    
                    # Create new game objects
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroid_field = AsteroidField()

            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_state = "menu"

        screen.fill('black')

        if game_state == "menu":
            draw_text_centered(screen, font, "ASTEROIDS", -50)
            draw_text_centered(screen, font, "Press ENTER to Start", 50)
        
        elif game_state == "playing":
            updatable.update(dt)

            # Collision checks
            for object in asteroids:
                if player.invulnerable_timer <= 0 and player.collides_with(object):
                    log_event("Player hit!")
                    lives -= 1
                    if lives <= 0:
                        game_state = "game_over"
                    else:
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity = pygame.Vector2(0, 0)
                        player.invulnerable_timer = 3
            
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("Asteroid hit!")
                        score += 10
                        asteroid.split()
                        shot.kill()

            for obj in drawable:
                obj.draw(screen)
            
            score_surface = font.render(f"Score: {score}", True, "white")
            lives_surface = font.render(f"Lives: {lives}", True, "white")
            screen.blit(score_surface, (10, 10))
            screen.blit(lives_surface, (10, 40))
            
            log_state() # Log state only while playing

        elif game_state == "game_over":
            draw_text_centered(screen, font, "GAME OVER", -50)
            draw_text_centered(screen, font, f"Final Score: {score}", 0)
            draw_text_centered(screen, font, "Press R to Restart", 50)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
