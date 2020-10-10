import pygame
from constants import SCREEN_HEIGHT


class Bird:
    BIRD_FLAP_EVENT = pygame.USEREVENT + 1

    def __init__(self):
        self.gravity = 0.2
        self.movement = 0

        upflap_surface = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
        midflap_surface = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
        downflap_surface = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
        self.frames = [upflap_surface, midflap_surface, downflap_surface]
        self.frame_index = 1

        self.surface = self.frames[self.frame_index]
        self.rect = self.surface.get_rect(center=(100, SCREEN_HEIGHT / 2))

    def start_flapping(self):
        pygame.time.set_timer(Bird.BIRD_FLAP_EVENT, 200)

    def flap(self):
        if self.frame_index < 2:
            self.frame_index += 1
        else:
            self.frame_index = 0

        prev_centery = self.rect.centery
        self.surface = self.frames[self.frame_index]
        self.rect = self.surface.get_rect(center=(100, prev_centery))

    def fall(self):
        self.movement += self.gravity
        self.rect.centery += self.movement

    def jump(self):
        self.movement = 0
        self.movement -= 8

    def clear_position(self):
        self.rect.center = (100, SCREEN_HEIGHT / 2)
        self.movement = 0

    def is_out_of_bounds(self):
        return self.rect.top <= -100 or self.rect.bottom >= 900

    def rotated(self):
        return pygame.transform.rotozoom(self.surface, - self.movement * 3, 1)
