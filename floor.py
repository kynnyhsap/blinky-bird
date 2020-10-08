import pygame

from constants import SCREEN_WIDTH


class Floor:
    def __init__(self):
        self.surface = pygame.image.load("assets/base.png").convert()
        self.surface = pygame.transform.scale2x(self.surface)
        self.x_position = 0

    def move(self):
        self.x_position -= 1
        if self.x_position <= -SCREEN_WIDTH:
            self.x_position = 0
