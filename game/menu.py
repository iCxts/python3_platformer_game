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