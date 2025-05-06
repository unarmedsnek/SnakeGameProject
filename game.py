# By Emilijus Kanapeckas

import pygame

import config
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

    # Method used for running the game and applying all its helper functions every frame
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

    # Helper method for the run method
    # Used for inputs and their handling
    # Basically assigning functionality to user inputs
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

            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "GAME OVER" and self.scoreboard_ui.restartbutton.is_clicked(
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

    # Helper method for the run method
    # Used for drawing the visuals
    def _draw(self):
        if self.game_state == "PLAYING":
            background_image = pygame.image.load(cf.BACKGROUND_IMAGE_MAINSCREEN)
            background_image = pygame.transform.scale(background_image, (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.scoreboard_ui.draw_score(self.screen)

        if self.game_state == "GAME OVER":
            background_image = pygame.image.load(cf.GAME_OVER_SCREEN)
            background_image = pygame.transform.scale(background_image, (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))

            self.scoreboard_ui.draw_game_over(self.screen)

        if self.game_state == "MENU":
            self.main_meniu.draw(self.screen)

        pygame.display.flip()

    # Helper method to the run method
    # Used for any updates that need to be applied every frame
    # All mechanicall moving parts of the code are located here
    def _update(self):
        self.snake.move()
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.get_body_segments())
            self.scoreboard.increase_score()
        if self.snake.check_collision_with_self() or self.snake.check_collision_with_wall():
            print("Game Over - Collision!")
            self.scoreboard.record_final_score()
            self.game_state = "GAME OVER"

    # Helper method that resets the game by initializing the snake, food classes
    # and calls the score to reset and spawns the first apple
    def _initialize_game_state(self):
        self.scoreboard.reset()
        self.food = Food()
        self.snake = Snake([20, 15])

        # Spawn the first apple
        self.food.spawn(self.snake.get_body_segments())