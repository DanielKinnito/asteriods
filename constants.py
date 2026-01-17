SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600
PLAYER_RADIUS = 20
LINE_WIDTH = 2
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
SHOT_RADIUS = 5
PLAYER_SHOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
PLAYER_ACCELERATION = 500
PLAYER_FRICTION = 0.5  # drag coefficient

# ============== EXPLOSION EFFECTS ==============
EXPLOSION_PARTICLE_COUNT = 20
EXPLOSION_PARTICLE_SPEED_MIN = 50
EXPLOSION_PARTICLE_SPEED_MAX = 200
EXPLOSION_DURATION = 0.8  # seconds
EXPLOSION_COLORS = [
    (255, 200, 50),   # bright yellow
    (255, 150, 30),   # orange
    (255, 100, 20),   # red-orange
    (255, 50, 10),    # red
    (150, 150, 150),  # gray (smoke)
]

# ============== BACKGROUND/STARFIELD ==============
STAR_LAYERS = 3
STARS_PER_LAYER = [100, 60, 30]  # far to near
STAR_SPEEDS = [0.1, 0.3, 0.6]    # parallax multipliers
STAR_SIZES = [1, 2, 3]           # pixel sizes
STAR_COLORS = [
    (100, 100, 120),  # dim blue-gray (far)
    (180, 180, 200),  # medium
    (255, 255, 255),  # bright white (near)
]

# ============== WEAPON TYPES ==============
WEAPON_STANDARD = 0
WEAPON_SPREAD = 1
WEAPON_RAPID = 2
WEAPON_LASER = 3

WEAPON_CONFIGS = {
    WEAPON_STANDARD: {
        "name": "Standard",
        "cooldown": 0.3,
        "shot_speed": 500,
        "shot_count": 1,
        "spread_angle": 0,
        "color": (255, 255, 100),  # yellow
        "damage": 1,
    },
    WEAPON_SPREAD: {
        "name": "Spread",
        "cooldown": 0.5,
        "shot_speed": 450,
        "shot_count": 3,
        "spread_angle": 15,
        "color": (100, 255, 100),  # green
        "damage": 1,
    },
    WEAPON_RAPID: {
        "name": "Rapid",
        "cooldown": 0.1,
        "shot_speed": 600,
        "shot_count": 1,
        "spread_angle": 0,
        "color": (255, 100, 100),  # red
        "damage": 0.5,
    },
    WEAPON_LASER: {
        "name": "Laser",
        "cooldown": 0.05,
        "shot_speed": 800,
        "shot_count": 1,
        "spread_angle": 0,
        "color": (100, 200, 255),  # cyan
        "damage": 0.3,
        "size": 2,  # smaller projectile
    },
}

# ============== BOMBS ==============
BOMB_RADIUS = 12
BOMB_FUSE_TIME = 2.0  # seconds
BOMB_EXPLOSION_RADIUS = 150
BOMB_MAX_COUNT = 3  # max bombs per life
BOMB_DROP_SPEED = 50  # backward velocity when dropped
BOMB_COLORS = [(255, 80, 80), (200, 50, 50)]  # blinking colors

# ============== POWER-UPS ==============
POWERUP_SPAWN_CHANCE = 0.25  # chance when asteroid destroyed
POWERUP_RADIUS = 15
POWERUP_FLOAT_SPEED = 1.5  # oscillation speed
POWERUP_FLOAT_AMPLITUDE = 5  # pixels

POWERUP_SHIELD = 0
POWERUP_SPEED = 1
POWERUP_WEAPON = 2

POWERUP_CONFIGS = {
    POWERUP_SHIELD: {
        "name": "Shield",
        "duration": 5.0,
        "color": (100, 150, 255),  # blue
        "icon": "S",
    },
    POWERUP_SPEED: {
        "name": "Speed",
        "duration": 8.0,
        "color": (255, 200, 50),   # gold
        "icon": "»",
        "speed_multiplier": 1.8,
    },
    POWERUP_WEAPON: {
        "name": "Weapon",
        "duration": 10.0,
        "color": (255, 100, 255),  # magenta
        "icon": "W",
    },
}

SHIELD_RING_RADIUS = 35  # visual shield effect

# ============== PLAYER BOOST (with speed power-up) ==============
PLAYER_SPEED_BOOST_MULTIPLIER = 1.8
PLAYER_ACCELERATION_BOOST = PLAYER_ACCELERATION * PLAYER_SPEED_BOOST_MULTIPLIER

# ============== ASTEROID LUMPINESS ==============
ASTEROID_VERTEX_COUNT = 10  # vertices for lumpy shape
ASTEROID_LUMP_VARIANCE = 0.3  # 0-1, how lumpy (0.3 = 30% variance)
ASTEROID_ROTATION_SPEED_MIN = 20  # degrees per second
ASTEROID_ROTATION_SPEED_MAX = 80
