import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()

        if image:
            self.image = image
        else:
            self.image = load_image(
                PLAYER_IMAGE,
                PLAYER_COLOR,
                (TILE_SIZE, TILE_SIZE)
            )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.last_jump_time = 0
        self.facing_right = True

    
    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # HORIZONTAL MOVEMENT
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        
        # VERTICAL MOVEMENT
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground and self.last_jump_time + JUMP_COOLDOWN < pygame.time.get_ticks():
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            self.last_jump_time = pygame.time.get_ticks()

        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        dy = self.vel_y

        # HORIZONTAL COLLISION
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right

        # VERTICAL COLLISION
        self.rect.y += dy
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = platform.rect.bottom

                self.vel_y = 0
    
    def draw(self, surface, camera_offset):
        surface.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))
        

