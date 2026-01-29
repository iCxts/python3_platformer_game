import pygame
import sys
import requests
from timer import Timer
from config import *
from player import Player
from menu import Menu, NameInputScreen, ResultScreen
from level import Level
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
camera_offset = [0, 0]

menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
name_input_screen = NameInputScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
result_screen = ResultScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
leaderboard_view = LeaderboardView(SCREEN_WIDTH, SCREEN_HEIGHT)
background = load_image(BACKGROUND_IMAGE, SKY_BLUE, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

timer = Timer()
network = Network()
opponent = Opponent()
player = None
level = None


def start_game():
    global player, level, camera_offset
    level = Level(f"level{current_level}.json")
    player = Player(level.spawn[0], level.spawn[1])
    camera_offset = [0, 0]


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
        hint_font = pygame.font.Font(None, 28)

        title = waiting_font.render("Multiplayer", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title, title_rect)

        status_text = "Waiting for opponent..."
        status = status_font.render(status_text, True, (150, 150, 150))
        status_rect = status.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(status, status_rect)

        hint_text = "Press ESC to cancel"
        hint = hint_font.render(hint_text, True, (100, 100, 100))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(hint, hint_rect)

        if network.matched:
            opponent.set_name(network.opponent_name)
            opponent.show()
            start_game()
            game_state = STATE_COUNTDOWN

        if network.opponent_disconnected:
            reset_to_menu()

    elif game_state == STATE_COUNTDOWN:
        screen.blit(background, (0, 0))

        if level and player:
            camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
            camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2
            level.draw(screen, camera_offset)
            player.draw(screen, camera_offset)
            opponent.update(network.opponent_pos)
            opponent.draw(screen, camera_offset)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        opponent_font = pygame.font.Font(None, 48)
        vs_text = opponent_font.render(f"VS  {network.opponent_name}", True, (255, 200, 100))
        vs_rect = vs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(vs_text, vs_rect)

        countdown_font = pygame.font.Font(None, 200)
        if network.countdown > 0:
            count_text = countdown_font.render(str(network.countdown), True, WHITE)
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(count_text, count_rect)

        ready_font = pygame.font.Font(None, 36)
        ready_text = ready_font.render("Get Ready!", True, (150, 150, 150))
        ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(ready_text, ready_rect)

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
        camera_offset[0] = player.rect.x - SCREEN_WIDTH // 2
        camera_offset[1] = player.rect.y - SCREEN_HEIGHT // 2

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

        if not is_multiplayer:
            level_font = pygame.font.Font(None, 28)
            level_text = level_font.render(f"Level {current_level}/{TOTAL_LEVELS}", True, WHITE)
            level_bg = pygame.Surface((level_text.get_width() + 20, level_text.get_height() + 10), pygame.SRCALPHA)
            level_bg.fill((0, 0, 0, 150))
            screen.blit(level_bg, (SCREEN_WIDTH - level_text.get_width() - 30, 15))
            screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 20))

        if is_multiplayer:
            vs_font = pygame.font.Font(None, 28)
            vs_text = vs_font.render(f"VS {network.opponent_name}", True, (255, 200, 100))
            vs_bg = pygame.Surface((vs_text.get_width() + 20, vs_text.get_height() + 10), pygame.SRCALPHA)
            vs_bg.fill((0, 0, 0, 150))
            screen.blit(vs_bg, (SCREEN_WIDTH - vs_text.get_width() - 30, 15))
            screen.blit(vs_text, (SCREEN_WIDTH - vs_text.get_width() - 20, 20))

            level_font = pygame.font.Font(None, 24)
            level_text = level_font.render(f"Level {current_level}/{TOTAL_LEVELS}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 50))

        if level.check_finish(player):
            current_level += 1
            if current_level <= TOTAL_LEVELS:
                start_game()
            else:
                final_time = timer.stop()
                if is_multiplayer:
                    network.send_finish(final_time)
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
            result_font = pygame.font.Font(None, 56)
            times_font = pygame.font.Font(None, 32)
            winner = network.race_result.get("winner", "")
            times = network.race_result.get("times", {})

            if winner == player_name:
                win_text = result_font.render("You Win!", True, (100, 255, 100))
            else:
                win_text = result_font.render(f"{winner} Wins!", True, (255, 100, 100))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
            screen.blit(win_text, win_rect)

            y_offset = 470
            for name, time_ms in sorted(times.items(), key=lambda x: x[1]):
                time_str = f"{name}: {time_ms // 1000:02d}:{(time_ms % 60000) // 1000:02d}.{time_ms % 1000:03d}"
                color = (100, 255, 100) if name == player_name else (200, 200, 200)
                time_text = times_font.render(time_str, True, color)
                time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(time_text, time_rect)
                y_offset += 35

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
