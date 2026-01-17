# Asteroids Game

A classic Asteroids arcade game clone implemented in Python using Pygame.

## Features

- **Space Ship Logic**: Navigate your ship with realistic physics including acceleration and deceleration.
- **Screen Wrapping**: Fly off one edge of the screen and appear on the opposite side.
- **Asteroid Field**: Survive an infinitely regenerating field of asteroids.
- **Shooting Mechanics**: Blast asteroids into smaller pieces to clear the field.
- **Scoring System**: Earn points for every asteroid destroyed.
- **Lives System**: You have 3 lives. Respawn in the center if you crash.

## Planned Features

- Explosions visuals
- Parallax background
- Multiple weapons
- Lumpy asteroid shapes
- Improved hitboxes
- Powerups
- Bombs

## Installation

Ensure you have Python 3.13 or newer installed. This project uses `uv` for dependency management.

1.  Clone the repository.
2.  Install dependencies and run:

    ```bash
    uv run main.py
    ```

    Or if using standard pip:

    ```bash
    pip install pygame
    python main.py
    ```

## Controls

- **W**: Thrust forward
- **A**: Rotate left
- **D**: Rotate right
- **S**: Reverse thrust / Brake
- **SPACE**: Shoot

## License

MIT License
