import pygame
import random

PIPE_HEIGHTS = (400, 500, 600)
DURATION = 1200
GAP = 300


class Pipes:
    SPAWN_PIPE_EVENT = pygame.USEREVENT

    def __init__(self):
        self.surface = pygame.image.load("assets/pipe-green.png").convert()
        self.surface = pygame.transform.scale2x(self.surface)

        self.pipes_list = []

    def start_spawning(self):
        pygame.time.set_timer(Pipes.SPAWN_PIPE_EVENT, DURATION)

    def shift_pipes(self):
        for pipe in self.pipes_list:
            pipe.centerx -= 5

    def spawn_new(self):
        pipe_y_position = random.choice(PIPE_HEIGHTS)

        bottom_pipe = self.surface.get_rect(midtop=(700, pipe_y_position))
        top_pipe = self.surface.get_rect(midbottom=(700, pipe_y_position - GAP))

        self.pipes_list.extend((bottom_pipe, top_pipe))

    def clear(self):
        self.pipes_list.clear()

    def is_collide_with_bird(self, bird):
        for pipe in self.pipes_list:
            if bird.rect.colliderect(pipe):
                return True

        return False
