import pygame
import sys
from config import *
from player import Player
from tiles import Platform

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player = Player(100, 100)
platforms = [
    Platform(0, 650, 1280, 70), 
    Platform(300, 500, 200, 20),
    Platform(600, 400, 200, 20)
]

camera_offset = [0, 0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    player.update(platforms)
    camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
    camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2

    screen.fill(SKY_BLUE)
    for platform in platforms:
        platform.draw(screen, camera_offset)
    player.draw(screen, camera_offset)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()