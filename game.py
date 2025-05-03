from operator import truediv

import pygame
import pygame as game
import config as cf
from scoreboard import Scoreboard


class GameSnake:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            pygame.event.pump()
            self.clock.tick(cf.GAME_SPEED)