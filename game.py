import pygame
import sys

from pygame.locals import *
from blinks import BlinkDetector
from bird import Bird
from pipes import Pipes
from floor import Floor

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Game:
    def __init__(self):
        self.blinks_detector = BlinkDetector()
        self.blinks_detector.start()

        pygame.init()
        pygame.event.set_allowed([
            QUIT,
            KEYDOWN,
            KEYUP,
            Pipes.SPAWN_PIPE_EVENT,
            Bird.BIRD_FLAP_EVENT
        ])

        self.active = True
        self.score = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
        self.screen.set_alpha(None)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('fonts/04B_19.ttf', 40)

        # Game objects
        self.bg_surface = pygame.transform.scale2x(pygame.image.load("assets/background-day.png").convert())
        self.gameover_surface = pygame.transform.scale2x(pygame.image.load("assets/gameover.png").convert_alpha())
        self.gameover_rect = self.gameover_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.floor = Floor()

        self.bird = Bird()
        self.bird.start_flapping()

        self.pipes = Pipes()
        self.pipes.start_spawning()

    def draw_score(self):
        surface = self.font.render(str(int(self.score)), True, (255, 255, 255))
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, 100))

        self.screen.blit(surface, rect)

    def draw_bg(self):
        self.screen.blit(self.bg_surface, (0, 0))

    def draw_gameover_message(self):
        self.screen.blit(self.gameover_surface, self.gameover_rect)

    def draw_floor(self):
        self.screen.blit(self.floor.surface, (self.floor.x_position, 900))
        self.screen.blit(self.floor.surface, (self.floor.x_position + SCREEN_WIDTH, 900))

    def draw_pipes(self):
        for pipe in self.pipes.pipes_list:
            if pipe.bottom >= SCREEN_HEIGHT:
                self.screen.blit(self.pipes.surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipes.surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def draw_bird(self):
        self.screen.blit(self.bird.rotated(), self.bird.rect)

    def check_collisions(self):
        return self.pipes.is_collide_with_bird(self.bird) or self.bird.is_out_of_bounds()

    def quit(self):
        self.blinks_detector.stop()
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            if self.blinks_detector.check_blinked() and self.active:
                self.bird.jump()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.active:
                        self.bird.jump()

                    if event.key == pygame.K_SPACE and not self.active:
                        self.active = True
                        self.score = 0
                        self.pipes.clear()
                        self.bird.clear_position()

                if event.type == Bird.BIRD_FLAP_EVENT:
                    self.bird.flap()

                if event.type == Pipes.SPAWN_PIPE_EVENT:
                    if self.active:
                        self.pipes.spawn_new()
                        self.score += 1

            self.draw_bg()

            if self.active:
                self.bird.fall()
                self.draw_bird()

                self.active = not self.check_collisions()

                self.pipes.shift_pipes()
                self.draw_pipes()
            else:
                self.draw_gameover_message()

            self.floor.move()
            self.draw_floor()

            self.draw_score()

            pygame.display.update()
            self.clock.tick(120)
