import pygame

pygame.init()

SCREEN_SIZE = (500, 650)
BIRD_SPEED = 1
ROCK_SPEED = 4
LIGHTING_SPEED = 2.5
FPS = 60

sky_image = pygame.image.load('images/sky_1.png')
sky_image = pygame.transform.scale(sky_image, SCREEN_SIZE)

GRASS_SIZE = (50, 50)

FONT = pygame.font.Font(None, 40)
