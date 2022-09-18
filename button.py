import pygame
pygame.init()


class Button:
    def __init__(self, surface, bg, fg, text, x, y, width, height, font, text_x, text_y,
                 font_size, border_color):
        self.surface = surface
        self.bg = bg
        self.fg = fg
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_x = text_x
        self.text_y = text_y
        self.font = font
        self.font_size = font_size
        self.border_color = border_color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_font = pygame.font.SysFont(self.font, self.font_size, "bold")

    def draw(self):
        self.text_font = pygame.font.SysFont(self.font, self.font_size, "bold")
        pygame.draw.rect(self.surface, self.bg, self.rect, 0, 15)
        pygame.draw.rect(self.surface, self.border_color, self.rect, 3, 15)
        self.surface.blit(self.text_font.render(self.text, True, self.fg), (self.text_x, self.text_y))
