import pygame
from config import *


class Camera:
    def __init__(self, level_width, level_height):
        self.offset = pygame.Vector2(0, 0)
        self.level_width = level_width
        self.level_height = level_height

    def update(self, target_rect):
        target_x = target_rect.centerx - SCREEN_WIDTH // 2
        target_y = target_rect.centery - SCREEN_HEIGHT // 2

        self.offset.x = max(0, min(target_x, self.level_width - SCREEN_WIDTH))
        self.offset.y = max(0, min(target_y, self.level_height - SCREEN_HEIGHT))

    def apply(self, rect):
        return pygame.Rect(
            rect.x - self.offset.x,
            rect.y - self.offset.y,
            rect.width,
            rect.height
        )

    def get_offset(self):
        return (int(self.offset.x), int(self.offset.y))

    def set_bounds(self, level_width, level_height):
        self.level_width = level_width
        self.level_height = level_height
