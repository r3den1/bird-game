import pygame
from settings import FONT


class Button:

    def __init__(self, pos: tuple[int, int], width: int, height: int, text: str):
        self.pos = pos
        self.width = width
        self.height = height
        self.buttonText = text

        self.colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333'
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.buttonSurface = FONT.render(self.buttonText, True, (255, 0, 0))

        self.pressed = False

    def update(self):
        mousepos = pygame.mouse.get_pos()
        self.buttonSurface = FONT.render(self.buttonText, True, self.colors['normal'])
        if self.buttonRect.collidepoint(mousepos):
            self.buttonSurface = FONT.render(self.buttonText, True, self.colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface = FONT.render(self.buttonText, True, self.colors['pressed'])
                self.pressed = True
        if self.pressed:
            self.pressed = False
            return self.buttonText, True
