#Abd Alah Fashesh

import pygame
import config

class Scoreboard:
    """
    Manages and displays the game score and game over message.
    """

    def __init__(self):
        """
        Initialize the scoreboard: fonts, colors, positions, and score.
        """
        self.score = 0  # Starting score

        # Initialize Pygame font module if not already initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # Create fonts for score and game-over messages
        self.font_score = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_SCORE
        )
        self.font_game_over = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_GAMEOVER
        )

        # Colors for rendering text
        self.score_text_color = config.SCORE_TEXT_COLOR
        self.game_over_text_color = config.GAME_OVER_TEXT_COLOR

        # Positions on screen
        self.score_position = (10, 10)
        self.game_over_position = (
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2
        )

    def reset(self) -> None:
        """
        Reset the score to zero for a new game.
        """
        self.score = 0

    def increase_score(self) -> None:
        """
        Called when the snake eats food: increments the score counter by 1.
        """
        self.score += 1

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the current score onto the given Pygame surface each frame.

        :param surface: The Pygame surface (screen) where text will be blitted.
        """
        score_text = f"Score: {self.score}"
        text_surf = self.font_score.render(
            score_text,                         # Text to render
            True,                                # Enable anti-aliasing
            self.score_text_color               # Color of the text
        )
        surface.blit(text_surf, self.score_position)  # Draw text at fixed position

    def draw_game_over(
        self,
        surface: pygame.Surface,
        message: str = "GAME OVER"
    ) -> None:
        """
        Draw a game over message and the final score when the game ends.

        :param surface: The Pygame surface (screen) where text will be blitted.
        :param message: The game over message to display (default "GAME OVER").
        """
        # Render and center the main message
        go_surf = self.font_game_over.render(
            message,                            # Message text
            True,                               # Enable anti-aliasing
            self.game_over_text_color          # Color for game-over text
        )
        go_rect = go_surf.get_rect(center=self.game_over_position)
        surface.blit(go_surf, go_rect)

        # Render and position the final score below the message
        final_text = f"Final Score: {self.score}"
        final_surf = self.font_score.render(
            final_text,
            True,
            self.score_text_color
        )
        # Compute dynamic spacing based on game-over font height
        spacing = self.font_game_over.get_height() + 10
        final_rect = final_surf.get_rect(
            center=(
                self.game_over_position[0],
                self.game_over_position[1] + spacing
            )
        )
        surface.blit(final_surf, final_rect)