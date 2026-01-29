import pygame
from config import *


class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed = 0
        self.running = False
        self.font = pygame.font.Font(None, 40)
        self.bg = load_image("ui/timer_bg.png", (0, 0, 0), (150, 50))
        self.bg = pygame.transform.scale(self.bg, (150, 50))
        self.bg.set_alpha(180)

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

    def draw(self, surface, x=20, y=20):
        surface.blit(self.bg, (x, y))
        time_str = self.format_time()
        text = self.font.render(time_str, True, WHITE)
        text_rect = text.get_rect(center=(x + 75, y + 25))
        surface.blit(text, text_rect)
