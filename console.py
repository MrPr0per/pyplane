import pygame

class Console:
    def __init__(self, font_size=12):
        self.font_size = font_size
        self.font_color = (0, 255, 0)
        self.font = pygame.font.SysFont("consolas", self.font_size)
        self.line_spacing = self.font_size * 1.5
        self.x = 10
        self.y = 20

    def draw_lines(self, sc:pygame.Surface, lines:list):
        for i, line in enumerate(lines):
            text = self.font.render(str(line), True, self.font_color)
            sc.blit(text, (self.x, self.y + i * self.line_spacing))