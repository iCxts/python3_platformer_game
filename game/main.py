import pygame
import sys
from timer import Timer
from config import *
from player import Player
from tiles import Platform
from menu import Menu
from level import Level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

current_level = 3
final_time = 0
game_state = STATE_MENU
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

def start_game():
    global player, level, camera_offset, timer
    level = Level(f"level{current_level}.json")
    player = Player(level.spawn[0], level.spawn[1])
    camera_offset = [0, 0]
    timer = Timer()

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
                current_level = 1
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
        keys = pygame.key.get_pressed()
        if not timer.running:
              if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or \
                keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_SPACE] or \
                keys[pygame.K_w] or keys[pygame.K_UP]:
                  timer.start()

        player.update(level.platforms)
        camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
        camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2

        level.draw(screen, camera_offset)
        player.draw(screen, camera_offset)
        timer.draw(screen)

        if level.check_finish(player):
            timer.stop()
            current_level += 1
            if current_level <= TOTAL_LEVELS:
                start_game()
            else:
                current_level = 1
                game_state = STATE_MENU


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()