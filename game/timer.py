import pygame
from config import *

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed = 0
        self.running = False
        self.font = pygame.font.Font(None, 48)
        self.bg = pygame.image.load(
            "game/assets/ui/timer_bg.png"
        ).convert_alpha()

    def start(self):
        if not self.running:
            self.start_time = pygame.time.get_ticks()
            self.running = True
    
    def stop(self):
        if self.running:
            self.elapsed += pygame.time.get_ticks() - self.start_time
            self.running = False
        return self.elapsed

    def reset(self):
        self.start_time = 0
        self.elapsed = 0
        self.running = False

    def get_time(self):
        if self.running:
            return pygame.time.get_ticks() - self.start_time
        return self.elapsed
    
    def format_time(self, ms=None):
        if ms is None:
            ms = self.get_time()
        seconds = ms // 1000
        millis = ms % 1000
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}.{millis:03d}"

    def draw(self, surface, x=10, y=10):
        time_str = self.format_time()
        text = self.font.render(time_str, True, WHITE)
        bg_rect = text.get_rect(topleft=(x, y))
        bg_rect.inflate_ip(10, 6)
        pygame.draw.rect(surface, BLACK, bg_rect, border_radius=4)
        surface.blit(text, (x, y))
        surface.blit(self.bg, (20, 20))
        surface.blit(text, (40, 30))