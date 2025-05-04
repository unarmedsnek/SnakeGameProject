#Ahmad Tomeh
#5/3/2025

import config
import random
import pygame
import snake
import game

class Food:
    def __init__(self):
        self.config = config
        self.snake = snake
        self.position = None

    def spawn(self, snake_body_segments=None):
        grid_width = self.config.GRID_WIDTH
        grid_height = self.config.GRID_HEIGHT

        while True:
            x = random.randrange(0, grid_width)
            y = random.randrange(0, grid_height)
            new_position = (x, y)

            if snake_body_segments is None or new_position not in snake_body_segments:
                self.position = new_position
                break

    def get_position(self):
        return self.position

    def draw(self, screen):
        if self.position:
            cell_size = config.CELL_SIZE
            food_color = config.FOOD_COLOR
            pixel_x = self.position[0] * cell_size
            pixel_y = self.position[1] * cell_size
            food_rect = pygame.Rect(pixel_x, pixel_y, cell_size, cell_size)
            pygame.draw.rect(screen, food_color, food_rect)