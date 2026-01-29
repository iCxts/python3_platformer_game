import pygame
from streamlit import image
from config import *

class Button:
    def __init__(self, x, y, text, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font = pygame.font.SysFont(None, 36)

    def update(self, mouse_pos):
        pass
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        text_surf = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

class Menu:
    def __init__(self, screen_width, screen_height):
        self.title_font = pygame.font.Font(None, 72)

        self.button_img = pygame.image.load(
            "game/assets/ui/button.png"
        ).convert_alpha()

        btn_w = self.button_img.get_width()
        btn_x = screen_width // 2 - btn_w // 2
        start_y = screen_height // 2 - 50
        spacing = 80

        self.buttons = {
            "singleplayer": Button(btn_x, start_y, "Singleplayer", self.button_img),
            "multiplayer": Button(btn_x, start_y + spacing, "Multiplayer", self.button_img),
            "leaderboards": Button(btn_x, start_y + 2 * spacing, "Leaderboards", self.button_img),
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
    
    def handle_click(self, mouse_pos, mouse_clicked):
        for name, btn in self.buttons.items():
            if btn.is_clicked(mouse_pos, mouse_clicked):
                return name
        return None 