# By Emilijus Kanapeckas

import pygame
import config as cf
from scoreboard import Scoreboard
from snake import Snake
from food import Food
from ui import MainMeniuScreen, ScoreboardUIScreen


class GameSnake:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.running = True
        self.clock = pygame.time.Clock()
        self.main_meniu = MainMeniuScreen()
        self.scoreboard = Scoreboard()
        self.scoreboard_ui = ScoreboardUIScreen(self.scoreboard)
        self._initialize_game_state()
        self.game_state = "MENU"  # Possible are MENIU, PLAYING, GAME_OVER
        head_pos = self.snake.get_head_position()
        segments = self.snake.get_body_segments()

        # Reset button
        button_width = 150  # Or your desired width
        button_height = 50  # Or your desired height
        button_x = (cf.SCREEN_WIDTH // 2) - (button_width // 2)
        button_y = (cf.SCREEN_HEIGHT // 2) + 200  # Adjust vertical position as needed
        self.restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    def run(self):

        # While loop to keep the game running
        while self.running:

            # Call the _handle_input helper method
            self._handle_input()

            # Call the _update helper class
            if self.game_state == "PLAYING":
                self._update()

            # Call the _draw helper method
            self._draw()

            self.clock.tick(cf.GAME_SPEED)

    def _handle_input(self):
        # Checks all the game events in the pygame.event.get() array
        for event in pygame.event.get():
            # If it finds that the user has quit the game it stops it
            if event.type == pygame.QUIT:
                self.running = False

            # If the player presses an arrow key the snakes direction changes
            if self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    if event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    if event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"

            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "GAME OVER" and self.restart_button_rect.collidepoint(
                    event.pos):
                print("RESTART BUTTON CLICKED")
                self.game_state = "PLAYING"
                self._initialize_game_state()

            if self.game_state == "MENU":
                action = self.main_meniu.handle_input(event)
                if action == "START":
                    self._initialize_game_state()
                    self.game_state = "PLAYING"
                elif action == "QUIT":
                    self.running = False

    # Helper class for drawing the visuals
    def _draw(self):
        # Draw the background
        # self.screen.fill(cf.BACKGROUND_COLOR)
        # pygame.draw.rect(self.screen, cf.WALL_COLOR, [0, 0, cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT], 2)
        if self.game_state == "PLAYING":
            background_image = pygame.image.load(cf.BACKGROUND_IMAGE)
            background_image = pygame.transform.scale(background_image, (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.scoreboard_ui.draw_score(self.screen)

        if self.game_state == "GAME OVER":
            self.scoreboard_ui.draw_game_over(self.screen)
            text_surf = self.scoreboard_ui.game_over_font.render("RESTART", True, cf.SCORE_TEXT_COLOR)
            text_rect = text_surf.get_rect()
            text_rect.center = self.restart_button_rect.center
            self.screen.blit(text_surf, text_rect)

        if self.game_state == "MENU":
            self.main_meniu.draw(self.screen)

        pygame.display.flip()

    def _update(self):
        # todo snake movement and everything that updates
        self.snake.move()
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.get_body_segments())
            self.scoreboard.increase_score()
        if self.snake.check_collision_with_self() or self.snake.check_collision_with_wall():
            print("Game Over - Collision!")
            self.scoreboard.record_final_score()
            self.game_state = "GAME OVER"

    def _initialize_game_state(self):
        self.scoreboard.reset()
        self.food = Food()
        self.snake = Snake([20, 15])

        # Spawn the first apple
        self.food.spawn(self.snake.get_body_segments())