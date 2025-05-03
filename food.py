#Ahmad Tomeh
import config
import random
import pygame
import snake
import game

class Food:
    def __init__(self, config):
        self.config = config
        self.position = None

    def spawn(self, snake_body_segments):
        grid_width = self.config.grid_width
        grid_height = self.config.grid_height

        while True:
            x = random.randrange(0, grid_width)
            y = random.randrange(0, grid_height)
            new_position = (x, y)
            if new_position not in snake_body_segments:
                self.position = new_position
                break

    def get_position(self):
        return self.position

    def draw(self, screen):
        if self.position:
            cell_size = self.config.cell_size
            food_color = self.config.food_color
            pixel_x = self.position[0] * cell_size
            pixel_y = self.position[1] * cell_size
            food_rect = pygame.Rect(pixel_x, pixel_y, cell_size, cell_size)
            pygame.draw.rect(screen, food_color, food_rect)

if __name__ == '__main__':
    # Example usage (for testing purposes only)
    class MockConfig:
        def __init__(self):
            self.grid_width = 20
            self.grid_height = 15
            self.cell_size = 30
            self.food_color = (255, 0, 0) # Red

    pygame.init()
    screen_width = MockConfig().grid_width * MockConfig().cell_size
    screen_height = MockConfig().grid_height * MockConfig().cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Food Test")
    clock = pygame.time.Clock()

    config = MockConfig()
    food = Food(config)
    snake_body = [(5, 5), (5, 6), (5, 7)] # Example snake body

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    food.spawn(snake_body)
                    print(f"Food spawned at: {food.get_position()}")

        screen.fill((0, 0, 0)) # Black background
        food.draw(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()