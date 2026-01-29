import pygame
import sys
import requests
from timer import Timer
from config import *
from player import Player
from menu import Menu, NameInputScreen, ResultScreen
from level import Level
from camera import Camera
from network import Network
from opponent import Opponent
from leaderboard_view import LeaderboardView

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

STATE_WAITING = "waiting"
STATE_COUNTDOWN = "countdown"
STATE_LEADERBOARD = "leaderboard"

current_level = 1
player_name = ""
game_state = STATE_MENU
is_multiplayer = False

menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
name_input_screen = NameInputScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
result_screen = ResultScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
leaderboard_view = LeaderboardView(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image(BACKGROUND_IMAGE, SKY_BLUE, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

timer = Timer()
network = Network()
opponent = Opponent()
camera = None
player = None
level = None


def start_game():
    global player, level, camera
    level = Level(f"level{current_level}.json")
    player = Player(level.spawn[0], level.spawn[1])
    level_width = 100 * TILE_SIZE
    level_height = 30 * TILE_SIZE
    camera = Camera(level_width, level_height)


def submit_score(name, time_ms):
    try:
        requests.post(
            f"{SERVER_URL}/api/leaderboard",
            json={"name": name, "time_ms": time_ms},
            timeout=5
        )
    except requests.exceptions.RequestException:
        pass


def reset_to_menu():
    global current_level, game_state, is_multiplayer
    current_level = 1
    timer.reset()
    network.disconnect()
    opponent.hide()
    is_multiplayer = False
    game_state = STATE_MENU


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
            if event.key == pygame.K_ESCAPE:
                if game_state in [STATE_PLAYING, STATE_WAITING, STATE_COUNTDOWN]:
                    reset_to_menu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True
        if game_state == STATE_NAME_INPUT:
            result = name_input_screen.handle_event(event)
            if result == "start":
                player_name = name_input_screen.player_name
                if is_multiplayer:
                    if network.connect():
                        network.join_queue(player_name)
                        game_state = STATE_WAITING
                    else:
                        game_state = STATE_MENU
                else:
                    start_game()
                    game_state = STATE_PLAYING

    if game_state == STATE_MENU:
        screen.fill(BLACK)
        menu.update(mouse_pos)
        menu.draw(screen)
        if mouse_click:
            clicked = menu.handle_click(mouse_pos, mouse_click)
            if clicked == "singleplayer":
                is_multiplayer = False
                game_state = STATE_NAME_INPUT
            elif clicked == "multiplayer":
                is_multiplayer = True
                game_state = STATE_NAME_INPUT
            elif clicked == "leaderboards":
                leaderboard_view.fetch()
                game_state = STATE_LEADERBOARD

    elif game_state == STATE_LEADERBOARD:
        screen.fill(BLACK)
        leaderboard_view.draw(screen)
        if mouse_click:
            clicked = leaderboard_view.handle_click(mouse_pos)
            if clicked == "back":
                game_state = STATE_MENU

    elif game_state == STATE_NAME_INPUT:
        screen.fill(BLACK)
        name_input_screen.update(mouse_pos)
        name_input_screen.draw(screen)
        if mouse_click:
            clicked = name_input_screen.handle_click(mouse_pos)
            if clicked == "start":
                player_name = name_input_screen.player_name
                if is_multiplayer:
                    if network.connect():
                        network.join_queue(player_name)
                        game_state = STATE_WAITING
                    else:
                        game_state = STATE_MENU
                else:
                    start_game()
                    game_state = STATE_PLAYING
            elif clicked == "back":
                game_state = STATE_MENU

    elif game_state == STATE_WAITING:
        screen.fill(BLACK)
        waiting_font = pygame.font.Font(None, 72)
        status_font = pygame.font.Font(None, 36)

        title = waiting_font.render("Multiplayer", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        status_text = "Waiting for opponent..."
        status = status_font.render(status_text, True, (150, 150, 150))
        status_rect = status.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(status, status_rect)

        if network.matched:
            opponent.set_name(network.opponent_name)
            opponent.show()
            start_game()
            game_state = STATE_COUNTDOWN

        if network.opponent_disconnected:
            reset_to_menu()

    elif game_state == STATE_COUNTDOWN:
        screen.blit(background, (0, 0))

        if level and player and camera:
            camera.update(player.rect)
            camera_offset = camera.get_offset()
            level.draw(screen, camera_offset)
            player.draw(screen, camera_offset)
            opponent.update(network.opponent_pos)
            opponent.draw(screen, camera_offset)

        countdown_font = pygame.font.Font(None, 200)
        if network.countdown > 0:
            count_text = countdown_font.render(str(network.countdown), True, WHITE)
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(count_text, count_rect)

        opponent_font = pygame.font.Font(None, 36)
        vs_text = opponent_font.render(f"VS {network.opponent_name}", True, (255, 200, 100))
        vs_rect = vs_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(vs_text, vs_rect)

        if network.race_started:
            timer.reset()
            timer.start()
            game_state = STATE_PLAYING

        if network.opponent_disconnected:
            reset_to_menu()

    elif game_state == STATE_PLAYING:
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()

        if not is_multiplayer and not timer.running:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or \
               keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_SPACE] or \
               keys[pygame.K_w] or keys[pygame.K_UP]:
                timer.start()

        player.update(level.platforms)
        camera.update(player.rect)
        camera_offset = camera.get_offset()

        if player.rect.y > level.death_height:
            player.rect.topleft = level.spawn

        if is_multiplayer:
            network.send_position(player.rect.x, player.rect.y)
            opponent.update(network.opponent_pos)

        level.draw(screen, camera_offset)

        if is_multiplayer:
            opponent.draw(screen, camera_offset)

        player.draw(screen, camera_offset)
        timer.draw(screen)

        if is_multiplayer:
            vs_font = pygame.font.Font(None, 28)
            vs_text = vs_font.render(f"VS {network.opponent_name}", True, (255, 200, 100))
            screen.blit(vs_text, (SCREEN_WIDTH - vs_text.get_width() - 20, 20))

        if level.check_finish(player):
            if is_multiplayer:
                final_time = timer.stop()
                network.send_finish(final_time)
                submit_score(player_name, final_time)
                result_screen.set_result(player_name, timer.format_time())
                game_state = STATE_RESULT
            else:
                current_level += 1
                if current_level <= TOTAL_LEVELS:
                    start_game()
                else:
                    final_time = timer.stop()
                    submit_score(player_name, final_time)
                    result_screen.set_result(player_name, timer.format_time())
                    game_state = STATE_RESULT

        if is_multiplayer and network.opponent_disconnected:
            final_time = timer.stop()
            result_screen.set_result(player_name, f"{timer.format_time()} (Opponent left)")
            game_state = STATE_RESULT

        if is_multiplayer and network.race_result:
            game_state = STATE_RESULT

    elif game_state == STATE_RESULT:
        screen.fill(BLACK)
        result_screen.update(mouse_pos)
        result_screen.draw(screen)

        if is_multiplayer and network.race_result:
            result_font = pygame.font.Font(None, 48)
            winner = network.race_result.get("winner", "")
            if winner == player_name:
                win_text = result_font.render("You Win!", True, (100, 255, 100))
            else:
                win_text = result_font.render(f"{winner} Wins!", True, (255, 100, 100))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
            screen.blit(win_text, win_rect)

        if mouse_click:
            clicked = result_screen.handle_click(mouse_pos)
            if clicked == "menu":
                reset_to_menu()
            elif clicked == "retry":
                if is_multiplayer:
                    network.reset()
                    if network.connect():
                        network.join_queue(player_name)
                        game_state = STATE_WAITING
                    else:
                        reset_to_menu()
                else:
                    current_level = 1
                    timer.reset()
                    start_game()
                    game_state = STATE_PLAYING

    pygame.display.flip()
    clock.tick(FPS)

network.disconnect()
pygame.quit()
sys.exit()
