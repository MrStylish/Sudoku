"""Imports pygame."""
import pygame

class Button:
    """classifies buttons."""
    def __init__(self, x, y, width, height, text=None, colour=(73, 73, 73), highlighted_colour=(189, 189, 189), function=None, params=None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colour
        self.highlighted_colour = highlighted_colour
        self.function = function
        self.params = params
        self.highlighted = False
        self.width = width
        self.height = height

    def update(self, mouse):
        """Highlights buttons when hovered."""
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        """Creates the buttons."""
        self.image.fill(self.highlighted_colour if self.highlighted else self.colour)
        if self.text:
            self.draw_text(self.text)
        window.blit(self.image, self.pos)

    def click(self):
        """Able to click on the buttons."""
        if self.params:
            self.function(self.params)
        else:
            self.function()

    def draw_text(self, text):
        """Able to put text in buttons."""
        font = pygame.font.SysFont("arial", 20, bold=1)
        text = font.render(text, False, (0, 0, 0))
        width, height = text.get_size()
        x = (self.width-width)//2
        y = (self.height-height)//2
        self.image.blit(text, (x, y))