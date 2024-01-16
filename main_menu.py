import pygame
from settings import SCREEN_SIZE
from buttons import Button

pygame.init()


class MainMenu:
    def __init__(self, image):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.image = image

        self.running = False

        self.button = Button((180, 400), 70, 50, 'level menu')

        self.level_button_pressed = False

    def run(self):
        while self.running:
            self.screen.blit(self.image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.blit(self.button.buttonSurface, self.button.pos)
            self.button.update()
            if self.button.update():
                self.level_button_pressed = True
                self.terminate()
            pygame.display.flip()

    def terminate(self):
        self.running = False
