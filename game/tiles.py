import pygame
from config import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, tile_type="platform"):
        super().__init__()

        tile_images = {
            "ground": "tiles/ground.png",
            "platform": "tiles/platform.png",
        }

        tile_path = tile_images.get(tile_type, "tiles/platform.png")
        tile_img = load_image(tile_path, PLATFORM_COLOR, (TILE_SIZE, TILE_SIZE))

        self.image = pygame.Surface((width, height))

        for ty in range(0, height, TILE_SIZE):
            for tx in range(0, width, TILE_SIZE):
                self.image.blit(tile_img, (tx, ty))

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface, camera_offset):
        surface.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))
