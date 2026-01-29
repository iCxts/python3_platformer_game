import pygame
import sys
from timer import Timer
from config import *
from player import Player
from tiles import Platform
from menu import Menu, NameInputScreen, ResultScreen
from level import Level
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

current_level = 1
player_name = ""
game_state = STATE_MENU
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
name_input_screen = NameInputScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
result_screen = ResultScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image(BACKGROUND_IMAGE, SKY_BLUE, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

timer = Timer()
def start_game():
    global player, level, camera_offset, timer
    level = Level(f"level{current_level}.json")
    player = Player(level.spawn[0], level.spawn[1])
    death_height = level.death_height
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
                current_level = 1
                timer.reset()
                game_state = STATE_MENU
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True
        if game_state == STATE_NAME_INPUT:
            result = name_input_screen.handle_event(event)
            if result == "start":
                player_name = name_input_screen.player_name
                start_game()
                game_state = STATE_PLAYING

    if game_state == STATE_MENU:
        screen.fill(BLACK)
        menu.update(mouse_pos)
        menu.draw(screen)
        if mouse_click:
            clicked = menu.handle_click(mouse_pos, mouse_click)
            if clicked == "singleplayer":
                game_state = STATE_NAME_INPUT
            elif clicked == "multiplayer":
                pass  # implement later
            elif clicked == "leaderboards":
                pass  # implement later

    elif game_state == STATE_NAME_INPUT:
        screen.fill(BLACK)
        name_input_screen.update(mouse_pos)
        name_input_screen.draw(screen)
        if mouse_click:
            clicked = name_input_screen.handle_click(mouse_pos)
            if clicked == "start":
                player_name = name_input_screen.player_name
                start_game()
                game_state = STATE_PLAYING
            elif clicked == "back":
                game_state = STATE_MENU
 
    elif game_state == STATE_PLAYING:
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        if not timer.running:
              if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or \
                keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_SPACE] or \
                keys[pygame.K_w] or keys[pygame.K_UP]:
                  timer.start()

        player.update(level.platforms)
        camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
        camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2

        if player.rect.y > level.death_height:
            player.rect.topleft = level.spawn
        
        #print(mouse_pos[0] + camera_offset[0], mouse_pos[1] + camera_offset[1])
       
        level.draw(screen, camera_offset)
        player.draw(screen, camera_offset)
        timer.draw(screen)

        if level.check_finish(player):
            current_level += 1
            if current_level <= TOTAL_LEVELS:
                start_game()
            else:
                timer.stop()
                result_screen.set_result(player_name, timer.format_time())
                game_state = STATE_RESULT

    elif game_state == STATE_RESULT:
        screen.fill(BLACK)
        result_screen.update(mouse_pos)
        result_screen.draw(screen)
        if mouse_click:
            clicked = result_screen.handle_click(mouse_pos)
            if clicked == "menu":
                current_level = 1
                timer.reset()
                game_state = STATE_MENU
            elif clicked == "retry":
                current_level = 1
                timer.reset()
                start_game()
                game_state = STATE_PLAYING

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
