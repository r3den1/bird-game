import pygame
from buttons import Button
from settings import sky_image, SCREEN_SIZE, FPS

pygame.init()


class LevelMenu:

    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.image = sky_image
        self.button_list = []
        self.back_button = Button((425, 0), 80, 40, 'back')
        self.running = False

        self.back_button_pressed = False

        self.chosen_level = None
        count = 0
        for i in range(1, 5):
            for j in range(1, 3):
                count += 1
                button = Button(pos=(100 * i, 100 * j + 150), width=50, height=50, text=str(count))
                self.button_list.append(button)

    def update(self, screen):
        level = None
        for button in self.button_list:
            screen.blit(button.buttonSurface, button.pos)
            button.update()
            if button.update():
                level = button.update()[0]
        screen.blit(self.back_button.buttonSurface, self.back_button.pos)
        self.back_button.update()
        return level

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.screen.blit(self.image, (0, 0))
            self.update(self.screen)

            back = self.back_button.update()
            if back:
                self.back_button_pressed = True
                self.terminate()

            level = self.update(self.screen)
            if level:
                self.chosen_level = level[0]
                self.terminate()

            pygame.time.Clock().tick(FPS)
            pygame.display.flip()

    def terminate(self):
        self.running = False
