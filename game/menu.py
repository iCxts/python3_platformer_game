import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER_COLOR
        self.font = pygame.font.SysFont(None, 36)
        self.hovered = False
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)

        text_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.hovered and mouse_clicked

class Menu:
    def __init__(self, screen_width, screen_height):
        self.title_font = pygame.font.Font(None, 72)

        btn_width, btn_height = 250, 50
        btn_x = screen_width // 2 - btn_width // 2
        start_y = screen_height // 2 - 50
        spacing = 70

        self.buttons = {
            "singleplayer": Button(btn_x, start_y, btn_width, btn_height, "Singleplayer"),
            "multiplayer": Button(btn_x, start_y + spacing, btn_width, btn_height, "Multiplayer"),
            "leaderboards": Button(btn_x, start_y + 2 * spacing, btn_width, btn_height, "Leaderboards"),
        }
    
    def update(self, mouse_pos):
        for btn in self.buttons.values():
            btn.update(mouse_pos)
    
    def draw(self, surface):
        title = self.title_font.render(TITLE, True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)

        for btn in self.buttons.values():
            btn.draw(surface)
    
    def handle_click(self, mouse_pos):
        for name, btn in self.buttons.items():
            if btn.is_clicked(mouse_pos, True):
                return name
        return None


class NameInputScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, 72)
        self.input_font = pygame.font.Font(None, 48)
        self.player_name = ""
        self.max_name_length = 12

        btn_width, btn_height = 200, 50
        btn_x = screen_width // 2 - btn_width // 2
        self.start_button = Button(btn_x, screen_height // 2 + 80, btn_width, btn_height, "Start")
        self.back_button = Button(btn_x, screen_height // 2 + 150, btn_width, btn_height, "Back")

        self.input_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 25, 300, 50)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN and self.player_name:
                return "start"
            elif len(self.player_name) < self.max_name_length and event.unicode.isprintable():
                self.player_name += event.unicode
        return None

    def update(self, mouse_pos):
        self.start_button.update(mouse_pos)
        self.back_button.update(mouse_pos)

    def draw(self, surface):
        title = self.title_font.render("Enter Your Name", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(title, title_rect)

        pygame.draw.rect(surface, WHITE, self.input_rect, 2, border_radius=8)

        name_surf = self.input_font.render(self.player_name, True, WHITE)
        name_rect = name_surf.get_rect(center=self.input_rect.center)
        surface.blit(name_surf, name_rect)

        if self.player_name:
            self.start_button.draw(surface)
        self.back_button.draw(surface)

    def handle_click(self, mouse_pos):
        if self.player_name and self.start_button.is_clicked(mouse_pos, True):
            return "start"
        if self.back_button.is_clicked(mouse_pos, True):
            return "back"
        return None


class ResultScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, 72)
        self.time_font = pygame.font.Font(None, 96)
        self.label_font = pygame.font.Font(None, 36)
        self.final_time = "00:00.000"
        self.player_name = ""

        btn_width, btn_height = 200, 50
        btn_x = screen_width // 2 - btn_width // 2
        self.menu_button = Button(btn_x, screen_height // 2 + 120, btn_width, btn_height, "Main Menu")
        self.retry_button = Button(btn_x, screen_height // 2 + 50, btn_width, btn_height, "Play Again")

    def set_result(self, player_name, final_time):
        self.player_name = player_name
        self.final_time = final_time

    def update(self, mouse_pos):
        self.menu_button.update(mouse_pos)
        self.retry_button.update(mouse_pos)

    def draw(self, surface):
        title = self.title_font.render("Level Complete!", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 120))
        surface.blit(title, title_rect)

        name_surf = self.label_font.render(f"Player: {self.player_name}", True, WHITE)
        name_rect = name_surf.get_rect(center=(self.screen_width // 2, 200))
        surface.blit(name_surf, name_rect)

        label = self.label_font.render("Final Time", True, WHITE)
        label_rect = label.get_rect(center=(self.screen_width // 2, 280))
        surface.blit(label, label_rect)

        time_surf = self.time_font.render(self.final_time, True, (100, 255, 100))
        time_rect = time_surf.get_rect(center=(self.screen_width // 2, 350))
        surface.blit(time_surf, time_rect)

        self.retry_button.draw(surface)
        self.menu_button.draw(surface)

    def handle_click(self, mouse_pos):
        if self.menu_button.is_clicked(mouse_pos, True):
            return "menu"
        if self.retry_button.is_clicked(mouse_pos, True):
            return "retry"
        return None