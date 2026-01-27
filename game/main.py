import pygame
import sys
from config import *
from player import Player
from tiles import Platform
from menu import Menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


game_state = STATE_MENU
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

def start_game():
    global player, platforms, camera_offset
    player = Player(100, 100)
    platforms = [
        Platform(0, 650, 1280, 70), 
        Platform(300, 500, 200, 20),
        Platform(600, 400, 200, 20)
    ]
    camera_offset = [0, 0]

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_ESCAPE and game_state == STATE_PLAYING:
                game_state = STATE_MENU
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True

    screen.fill(SKY_BLUE)
    if game_state == STATE_MENU:
        menu.update(mouse_pos)
        menu.draw(screen)
        if mouse_click:
            clicked = menu.handle_click(mouse_pos)
            if clicked == "singleplayer":
                start_game()
                game_state = STATE_PLAYING
            elif clicked == "multiplayer":
                pass # implement later
            elif clicked == "leaderboards":
                pass # implement later
    
    elif game_state == STATE_PLAYING:
        player.update(platforms)
        camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
        camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2

        for platform in platforms:
            platform.draw(screen, camera_offset)
        player.draw(screen, camera_offset)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()