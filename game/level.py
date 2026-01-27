import pygame
import json
import os
from config import *
from tiles import Platform

class FinishLine(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        for row in range(0, height, 16):
            for col in range(0, width, 16):
                color = WHITE if (row + col) // 16 % 2 == 0 else BLACK
                pygame.draw.rect(self.image, color, (col, row, 16, 16))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface, camera_offset):
        surface.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

class Level:
    def __init__(self, filename):
        self.platforms = []
        self.finish_line = None
        self.name = ""
        self.load(filename)
    
    def load(self, filename):
        path = os.path.join(LEVELS_DIR, filename)
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.name = data.get("name", "Unnamed Level")
        tile_size = data.get("tile_size", TILE_SIZE)

        spawn = data.get("spawn", {"x": 0, "y": 0})
        self.spawn = (spawn["x"] * tile_size, spawn["y"] * tile_size)

        finish = data.get("finish", {"x": 100, "y": 16})
        self.finish_line = FinishLine(
            finish["x"] * tile_size,
            finish["y"] * tile_size,
            tile_size * 2,
            tile_size * 2
        )

        for tile in data.get("tiles", []):
            x = tile["x"] * tile_size
            y = tile["y"] * tile_size
            width = tile.get("width", 1) * tile_size
            height = tile.get("height", 1) * tile_size
            self.platforms.append(Platform(x, y, width, height))

    def check_finish(self, player):
        return player.rect.colliderect(self.finish_line.rect)
        
    def draw(self, surface, camera_offset):
        for platform in self.platforms:
            platform.draw(surface, camera_offset)
            
        self.finish_line.draw(surface, camera_offset)
    

    