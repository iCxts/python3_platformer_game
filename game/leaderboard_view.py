import pygame
import requests
from config import *


class LeaderboardView:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, 72)
        self.header_font = pygame.font.Font(None, 36)
        self.entry_font = pygame.font.Font(None, 32)
        self.entries = []
        self.loading = False
        self.error = None

        btn_width, btn_height = 200, 50
        btn_x = screen_width // 2 - btn_width // 2
        self.back_button = pygame.Rect(btn_x, screen_height - 100, btn_width, btn_height)

    def fetch(self):
        self.loading = True
        self.error = None
        try:
            response = requests.get(f"{SERVER_URL}/api/leaderboard", timeout=5)
            if response.status_code == 200:
                self.entries = response.json()
            else:
                self.error = "Failed to load leaderboard"
        except requests.exceptions.RequestException:
            self.error = "Could not connect to server"
        finally:
            self.loading = False

    def format_time(self, time_ms):
        seconds = time_ms // 1000
        millis = time_ms % 1000
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}.{millis:03d}"

    def draw(self, surface):
        title = self.title_font.render("Leaderboard", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title, title_rect)

        if self.loading:
            loading_text = self.header_font.render("Loading...", True, WHITE)
            loading_rect = loading_text.get_rect(center=(self.screen_width // 2, 200))
            surface.blit(loading_text, loading_rect)
            return

        if self.error:
            error_text = self.header_font.render(self.error, True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(self.screen_width // 2, 200))
            surface.blit(error_text, error_rect)
        elif not self.entries:
            empty_text = self.header_font.render("No scores yet!", True, WHITE)
            empty_rect = empty_text.get_rect(center=(self.screen_width // 2, 200))
            surface.blit(empty_text, empty_rect)
        else:
            header_y = 150
            rank_text = self.header_font.render("Rank", True, (150, 150, 150))
            name_text = self.header_font.render("Player", True, (150, 150, 150))
            time_text = self.header_font.render("Time", True, (150, 150, 150))

            surface.blit(rank_text, (self.screen_width // 2 - 250, header_y))
            surface.blit(name_text, (self.screen_width // 2 - 100, header_y))
            surface.blit(time_text, (self.screen_width // 2 + 150, header_y))

            for i, entry in enumerate(self.entries[:10]):
                y = 200 + i * 40

                if i == 0:
                    color = (255, 215, 0)
                elif i == 1:
                    color = (192, 192, 192)
                elif i == 2:
                    color = (205, 127, 50)
                else:
                    color = WHITE

                rank_surf = self.entry_font.render(f"#{i + 1}", True, color)
                name_surf = self.entry_font.render(entry["player_name"], True, color)
                time_surf = self.entry_font.render(self.format_time(entry["time_ms"]), True, color)

                surface.blit(rank_surf, (self.screen_width // 2 - 250, y))
                surface.blit(name_surf, (self.screen_width // 2 - 100, y))
                surface.blit(time_surf, (self.screen_width // 2 + 150, y))

        pygame.draw.rect(surface, BUTTON_COLOR, self.back_button, border_radius=8)
        back_text = self.header_font.render("Back", True, WHITE)
        back_rect = back_text.get_rect(center=self.back_button.center)
        surface.blit(back_text, back_rect)

    def handle_click(self, mouse_pos):
        if self.back_button.collidepoint(mouse_pos):
            return "back"
        return None
