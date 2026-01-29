import pygame
from config import *


class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("sprites/opponent.png", (255, 100, 100), (TILE_SIZE, TILE_SIZE))
        self.image.set_alpha(GHOST_ALPHA)
        self.rect = self.image.get_rect()
        self.visible = False
        self.name = ""
        self.font = pygame.font.Font(None, 24)

    def update(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def set_name(self, name):
        self.name = name

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surface, camera_offset):
        if not self.visible:
            return

        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]

        surface.blit(self.image, (draw_x, draw_y))

        if self.name:
            name_surf = self.font.render(self.name, True, WHITE)
            name_rect = name_surf.get_rect(centerx=draw_x + TILE_SIZE // 2, bottom=draw_y - 5)
            surface.blit(name_surf, name_rect)
