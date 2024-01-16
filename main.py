from main_menu import MainMenu
from settings import SCREEN_SIZE, FPS, BIRD_SPEED, ROCK_SPEED, GRASS_SIZE, sky_image, LIGHTING_SPEED
import pygame
from buttons import Button
from level_menu import LevelMenu

pygame.display.set_mode(SCREEN_SIZE, 0, 0)

lighting_image = pygame.image.load('images/lighting.png')
lighting_image = pygame.transform.scale(lighting_image, (50, 50))

platform_image = pygame.image.load('images/platform.png')
platform_image = pygame.transform.scale(platform_image, (50, 50))

line_image = pygame.image.load('images/line_1.png')
line_image = pygame.transform.scale(line_image, (SCREEN_SIZE[1] + GRASS_SIZE[0], 50))

bird_image = pygame.image.load('images/bird_1.png').convert_alpha()
bird_image = pygame.transform.scale(bird_image, (50, 50))

rock_image = pygame.image.load('images/rock_2.png').convert_alpha()
rock_image = pygame.transform.scale(rock_image, (30, 30))

grass_image = pygame.image.load('images/grass_1.png').convert_alpha()
grass_image = pygame.transform.scale(grass_image, (50, 50))

post_image = pygame.image.load('images/post_1.png')
post_image = pygame.transform.scale(post_image, (50, 50))

win_image = pygame.image.load('images/win_image.png').convert_alpha()
win_image = pygame.transform.scale(win_image, (300, 300))

lose_image = pygame.image.load('images/lose_image.png')
lose_image = pygame.transform.scale(lose_image, (300, 300))

posts_group = pygame.sprite.Group()
birds_group = pygame.sprite.Group()
rocks_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lighting_group = pygame.sprite.Group()
win_group = pygame.sprite.Group()
lose_group = pygame.sprite.Group()


def load_level(level_number: str):
    try:
        path = f'levels/level_{level_number}'
        with open(path, 'r') as file:
            level_map = [line.strip() for line in file]

        return level_map
    except FileNotFoundError:
        print(f'похоже, такого уровня еще не существует...')


def generate_level(lvl: list):
    for line in range(len(lvl)):
        for i in range(len(lvl[line])):

            if lvl[line][i] == 'l':
                Lighting((GRASS_SIZE[0] * i - GRASS_SIZE[0], SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 2)),
                         allgroup=all_group, lightinggroup=lighting_group)
            if lvl[line][i] == 'L':
                Line((GRASS_SIZE[0] * i - GRASS_SIZE[0], SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 2)),
                     allgroup=all_group)
            if lvl[line][i] == 'p':
                Platform((GRASS_SIZE[0] * i, SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 1)),
                         allgroup=all_group,
                         platformgroup=platform_group)
            if lvl[line][i] == 'G':
                Grass((GRASS_SIZE[0] * i, SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 1)),
                      allgroup=all_group)
            if lvl[line][i] == 'P':
                Tree((post_image.get_width() * i, SCREEN_SIZE[1] - post_image.get_height() - line * GRASS_SIZE[0]),
                     post_group=posts_group,
                     allgroup=all_group)
            if lvl[line][i] == 'B':
                Bird(
                    (GRASS_SIZE[0] * i, SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 2)),
                    bird_group=birds_group,
                    post_group=posts_group,
                    rock_group=rocks_group,
                    allgroup=all_group)
            if lvl[line][i] == 'b':
                Bird(
                    (GRASS_SIZE[0] * i, SCREEN_SIZE[1] - GRASS_SIZE[1] * (line + 2)),
                    bird_group=birds_group,
                    post_group=posts_group,
                    rock_group=rocks_group,
                    allgroup=all_group, reverse=True)
    rock = Rock((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - GRASS_SIZE[1]),
                rock_group=rocks_group,
                allgroup=all_group,
                platformgroup=platform_group,
                lightinggroup=lighting_group)
    return rock


class Bird(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], post_group, allgroup, rock_group, bird_group, reverse=False):
        super().__init__(allgroup, bird_group)
        self.pos = pos
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

        self.transformed_image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        self.post = post_group
        self.rock = rock_group
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = BIRD_SPEED if reverse else -BIRD_SPEED

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.speed, 0)
        for post in self.post:
            if pygame.sprite.collide_mask(self, post):
                self.speed *= -1
        if self.speed > 0:
            self.image = self.transformed_image
        if self.speed < 0:
            self.image = bird_image
        for rock in self.rock:
            if pygame.sprite.collide_mask(self, rock):
                self.kill()
                return True
        if self.rect.x == SCREEN_SIZE[0] - self.rect.width:
            self.speed *= -1
            self.image = self.transformed_image
        if self.rect.x == 0:
            self.speed *= -1
            self.image = bird_image


class Rock(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], rock_group, allgroup, platformgroup, lightinggroup):
        super().__init__(rock_group, allgroup)

        self.pos = pos

        self.image = rock_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

        self.platform_group = platformgroup
        self.lighting = lightinggroup

        self.speed_y = 0
        self.speed_x = 0
        self.rock_speed = -ROCK_SPEED

        self.activated = False
        self.activate_count = 0
        self.out_of_screen = False

    def update(self, pos: tuple[int, int] = None):
        self.rect = self.rect.move(self.speed_x, self.speed_y)

        if pos:
            if pos[1] > SCREEN_SIZE[1] - GRASS_SIZE[1]:
                pos = pos[0], SCREEN_SIZE[1] - GRASS_SIZE[1]

        if (not self.activated) and pos:
            self.rect.x, self.rect.y = pos[0], self.rect.y
        elif self.activated and self.activate_count == 0:
            self.activate_count += 1
            self.speed_y = self.rock_speed

        if self.rect.y > SCREEN_SIZE[1] or self.rect.y < 0:
            self.kill()

        for lighting in self.lighting:
            if pygame.sprite.collide_mask(self, lighting):
                self.kill()

        for platform in self.platform_group:
            if pygame.sprite.collide_mask(self, platform):
                self.speed_y *= -1


class Grass(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], allgroup):
        super().__init__(allgroup)

        self.image = grass_image

        self.rect = self.image.get_rect()

        self.pos = pos

        self.rect.x, self.rect.y = self.pos[0], self.pos[1]


class Tree(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], post_group, allgroup):
        super().__init__(post_group, allgroup)

        self.image = post_image

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]


class Platform(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], allgroup, platformgroup):
        super().__init__(allgroup, platformgroup)

        self.pos = pos

        self.image = platform_image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos[0], self.pos[1]


class Line(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], allgroup):
        super().__init__(allgroup)
        self.pos = pos

        self.image = line_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]


class Lighting(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int], allgroup, lightinggroup):
        super().__init__(allgroup, lightinggroup)
        self.image = lighting_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]

        self.speed = LIGHTING_SPEED

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(self.speed, 0)

        if self.rect.x > SCREEN_SIZE[0]:
            self.speed *= -1
        if self.rect.x < 0:
            self.speed *= -1


class Win(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int] = (100, 0), wingroup: pygame.sprite.Group = win_group):
        super().__init__(wingroup, all_group)
        self.image = win_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]


class Lose(pygame.sprite.Sprite):

    def __init__(self, pos: tuple[int, int] = (100, 0), losegroup: pygame.sprite.Group = lose_group):
        super().__init__(losegroup, all_group)

        self.image = lose_image

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = pos[0], pos[1]


class MainScene:

    def __init__(self, size: tuple[int, int], lvl: list):
        self.size = size
        self.screen = pygame.display.set_mode(size)

        self.level = lvl
        self.clock = pygame.time.Clock()
        self.back_button = Button((425, 0), 80, 40, 'menu')
        self.win = False
        self.lose = False

        self.back_button_pressed = False
        self.running = False

        self.mouse_pos = None

    def run(self):

        rock = generate_level(self.level)
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rock.activated = True
                if event.type == pygame.MOUSEMOTION and rock.activated is False:
                    if pygame.mouse.get_pos():
                        self.mouse_pos = pygame.mouse.get_pos()
            if len(rocks_group.sprites()) == 0:
                self.lose = True

            if rock.out_of_screen:
                self.lose = True
            if len(birds_group.sprites()) == 0:
                self.win = True

            self.update()
            self.screen.blit(self.back_button.buttonSurface, self.back_button.pos)
            self.back_button.update()

            back = self.back_button.update()
            if back:
                self.back_button_pressed = True
                self.terminate()

            self.draw()
            self.screen.blit(self.back_button.buttonSurface, self.back_button.pos)
            self.back_button.update()
            self.clock.tick(FPS)
            pygame.display.flip()

    def update(self):
        if self.win and not self.lose:
            Win(wingroup=win_group)
        if self.lose and not self.win:
            Lose(losegroup=lose_group)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(sky_image, (0, 0))
        all_group.draw(self.screen)
        all_group.update(self.mouse_pos)
        win_group.draw(self.screen)
        lose_group.draw(self.screen)

    def terminate(self):
        self.running = False


if __name__ == '__main__':
    main = None
    menu = MainMenu(sky_image)
    menu.running = True
    menu.run()
    level_menu = LevelMenu()
    while True:
        if level_menu.back_button_pressed:
            level_menu.back_button_pressed = False
            menu.running = True
            menu.run()
        if menu.level_button_pressed:
            menu.level_button_pressed = False
            level_menu.running = True
            level_menu.run()

        if level_menu.chosen_level:
            level = level_menu.chosen_level
            level_menu.chosen_level = None
            loaded_level = load_level(level)
            if loaded_level:
                for i in all_group.sprites():
                    i.kill()
                main = MainScene(SCREEN_SIZE, loaded_level)
                main.running = True
                main.run()
            else:
                level_menu.running = True
                level_menu.run()

        if main:
            if main.back_button_pressed:
                main.back_button_pressed = False
                level_menu.running = True
                level_menu.run()
