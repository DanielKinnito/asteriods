import sys
import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    print("Starting Asteroids Game with Pygame version:", pygame.__version__)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for object in asteroids:
            if player.invulnerable_timer <= 0 and player.collides_with(object):
                log_event("Player hit!")
                lives -= 1
                if lives <= 0:
                    print("Game Over! Player collided with an asteroid.")
                    sys.exit()
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

        screen.fill('black')

        for obj in drawable:
            obj.draw(screen)
        
        score_surface = font.render(f"Score: {score}", True, "white")
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_surface, (10, 10))
        screen.blit(lives_surface, (10, 40))

        pygame.display.flip()


        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

        log_state()


if __name__ == "__main__":
    main()
