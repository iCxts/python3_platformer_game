import os
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "meowmeowcat92's Platformer Game"
TOTAL_LEVELS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PLAYER_COLOR = (50, 150, 255)
PLAYER_IMAGE = "sprites/player.png"
BACKGROUND_IMAGE = "backgrounds/background.png"
PLATFORM_COLOR = (0, 0, 0)
GHOST_ALPHA = 100

STATE_MENU = "menu"
STATE_NAME_INPUT = "name_input"
STATE_PLAYING = "playing"
STATE_RESULT = "result"

BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
BUTTON_TEXT_COLOR = WHITE

GRAVITY = 0.5
JUMP_STRENGTH = -13
JUMP_COOLDOWN = 150
PLAYER_SPEED = 5
MAX_FALL_SPEED = 15

TILE_SIZE = 32
DEATH_Y_LEVEL = 20 * TILE_SIZE

SERVER_URL = "http://localhost:5000"

COUNTDOWN_SECONDS = 3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")


def load_image(path, fallback_color, fallback_size):
    """Load an image from the assets directory, or create a colored fallback surface."""
    full_path = os.path.join(ASSETS_DIR, path)
    if os.path.exists(full_path):
        return pygame.image.load(full_path).convert_alpha()
    surf = pygame.Surface(fallback_size)
    surf.fill(fallback_color)
    return surf
