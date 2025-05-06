
import pygame
import config as cf
from scoreboard import Scoreboard  # Already there
from snake import Snake             # Already there
from food import Food               # Already there
from ui import MainMenuScreen       # Change MainMeniuScreen to MainMenuScreen if you renamed the class

class GameSnake:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.running = True
        self.clock = pygame.time.Clock()

        # --- MODIFICATION: Initialize Scoreboard first ---
        self.scoreboard = Scoreboard()
        # --- MODIFICATION: Pass scoreboard instance to MainMenuScreen ---
        self.main_menu = MainMenuScreen(self.scoreboard)  # Corrected class name if you used MainMenuScreen

        # self._initialize_game_state() # Called when transitioning to PLAYING
        self.game_state = "MENU"  # Possible states: MENU, PLAYING, GAME_OVER

        # Reset button for GAME_OVER state
        button_width = 150
        button_height = 50
        button_x = (cf.SCREEN_WIDTH // 2) - (button_width // 2)
        # --- MODIFICATION: Adjust Y position of restart button if scoreboard table is tall ---
        # This might need dynamic adjustment based on scoreboard.draw_game_over_screen's content height
        button_y = cf.SCREEN_HEIGHT - button_height - 30  # Positioned towards the bottom
        self.restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.restart_button_font = pygame.font.SysFont(cf.FONT_NAME, cf.BUTTON_FONT_SIZE)

    # ... (run method remains the same) ...
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                        # When returning to menu, good to reset current game score if it was in progress
                        self.scoreboard.reset_current_game_score()


            elif self.game_state == "GAME OVER":
                # --- MODIFICATION: Handle restart button click ---
                if event.type == pygame.MOUSEBUTTONDOWN and self.restart_button_rect.collidepoint(event.pos):
                    # Ensure a player is active before restarting
                    if not self.scoreboard.current_player_name and self.scoreboard.players:
                        # If no specific current player, pick the first one from the list
                        first_player_name = list(self.scoreboard.players.keys())[0]
                        self.scoreboard.set_current_player(first_player_name)

                    if self.scoreboard.current_player_name:  # Only start if a player is set
                        self._initialize_game_state()  # Resets snake, food, score
                        self.game_state = "PLAYING"
                    else:
                        # Optionally, stay in GAME OVER or switch to MENU if no player can be set
                        # For simplicity, we assume UI flow ensures a player exists if game was played.
                        # If coming from a game, current_player_name should be set.
                        # If trying to restart after app launch without playing, this might be an issue.
                        # Let's assume normal flow: Menu -> Add Player -> Start -> Game Over -> Restart
                        pass


            elif self.game_state == "MENU":
                # --- MODIFICATION: MainMenuScreen handles its own input, returns action ---
                action = self.main_menu.handle_input(event)
                if action == "START":
                    # --- MODIFICATION: Logic to ensure a player is selected/active ---
                    if not self.scoreboard.current_player_name and self.scoreboard.players:
                        # If no player is 'current' (e.g., after app start, before adding/selecting)
                        # but players exist (e.g., from previous additions in this session),
                        # set the first available player as current.
                        first_player_name = list(self.scoreboard.players.keys())[0]
                        self.scoreboard.set_current_player(first_player_name)
                        print(f"No current player, auto-selected: {self.scoreboard.current_player_name}")

                    if self.scoreboard.current_player_name:  # Check if a player is ready
                        self._initialize_game_state()
                        self.game_state = "PLAYING"
                        print(f"Starting game for player: {self.scoreboard.current_player_name}")
                    else:
                        # No player active/added - optionally show a message on screen
                        print("No player selected or added. Please add a player from the menu.")
                        # Stay in "MENU" state
                        pass
                elif action == "QUIT":
                    self.running = False

    def _draw(self):
        if self.game_state == "PLAYING":
            # Load and draw background image
            try:
                background_image = pygame.image.load(cf.BACKGROUND_IMAGE)
                background_image = pygame.transform.scale(background_image, (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
                self.screen.blit(background_image, (0, 0))
            except pygame.error as e:  # Handle if image fails to load
                print(f"Error loading background image: {e}. Using solid color.")
                self.screen.fill(cf.BACKGROUND_COLOR)  # Fallback to solid color

            # Draw game elements
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            # --- MODIFICATION: Use new scoreboard draw method for live score ---
            self.scoreboard.draw_live_score(self.screen)

        elif self.game_state == "GAME OVER":
            # --- MODIFICATION: Use new scoreboard method for game over screen ---
            # Fill screen, or draw a game over background
            self.screen.fill(cf.BACKGROUND_COLOR)  # Example: Simple black background for game over
            self.scoreboard.draw_game_over_screen(self.screen)  # This now draws all game over info

            # --- MODIFICATION: Draw Restart Button ---
            pygame.draw.rect(self.screen, (0, 150, 0), self.restart_button_rect, border_radius=5)  # Green button
            restart_text_surf = self.restart_button_font.render("RESTART", True,
                                                                cf.BUTTON_TEXT_COLOR)  # Use config color
            restart_text_rect = restart_text_surf.get_rect(center=self.restart_button_rect.center)
            self.screen.blit(restart_text_surf, restart_text_rect)

        elif self.game_state == "MENU":
            # --- MODIFICATION: MainMenuScreen's draw method handles all menu UI ---
            self.screen.fill(cf.BACKGROUND_COLOR)  # Clear screen for menu
            self.main_menu.draw(self.screen)

        pygame.display.flip()

    def _update(self):
        self.snake.move()
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.get_body_segments())
            # --- MODIFICATION: Scoreboard handles score increase ---
            self.scoreboard.increase_score()

        if self.snake.check_collision_with_self() or self.snake.check_collision_with_wall():
            print(
                f"Game Over for player: {self.scoreboard.current_player_name} - Collision! Final Score for this game: {self.scoreboard.score}")
            # --- MODIFICATION: Scoreboard records the final score against the current player ---
            self.scoreboard.record_final_score()  # This updates the player's session best if current score is higher
            self.game_state = "GAME OVER"

    def _initialize_game_state(self):
        # --- MODIFICATION: Reset current game's score in scoreboard ---
        self.scoreboard.reset_current_game_score()  # Resets self.score to 0

        # Initialize food and snake
        self.food = Food()
        # Assuming initial_position for Snake is a list/tuple like [grid_x, grid_y]
        initial_snake_pos_grid = [cf.GRID_WIDTH // 2, cf.GRID_HEIGHT // 2]  # Example starting position
        self.snake = Snake(initial_snake_pos_grid)

        # Spawn the first food item, ensuring it's not under the snake
        self.food.spawn(self.snake.get_body_segments())

        # Ensure game state is set to playing if this method is called to start a game
        # self.game_state = "PLAYING" # This is usually set by the caller like _handle_input