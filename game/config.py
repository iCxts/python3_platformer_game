SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "meowmeowcat92's Platformer Game"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PLAYER_COLOR = (50, 150, 255)
PLATFORM_COLOR = (0, 0, 0)
GHOST_ALPHA = 100

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_RESULT ="result"

BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = WHITE

GRAVITY = 0.5
JUMP_STRENGTH = -15
JUMP_COOLDOWN = 300
PLAYER_SPEED = 5
MAX_FALL_SPEED = 15

TILE_SIZE = 32


SERVER_URL = "http://localhost:5000"

COUNTDOWN_SECONDS = 3

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

def load_image(path, fallback_color, fallback_size):
    """Load PNG if exists, otherwise create colored rect."""
    import pygame
    full_path = os.path.join(ASSETS_DIR, path)
    if os.path.exists(full_path):
        return pygame.image.load(full_path).convert_alpha()
    else:
        surf = pygame.Surface(fallback_size)
        surf.fill(fallback_color)
        return surf