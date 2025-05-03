#Abd Alah Fashesh
import pygame
import config


class Scoreboard:
    def __init__(self):
        self.score = 0

        pygame.font.init()

        self.font_score = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SCORE)
        self.font_game_over = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_GAMEOVER)

        self.score_text_color = config.SCORE_TEXT_COLOR
        self.game_over_text_color = config.GAME_OVER_TEXT_COLOR

        self.score_position = (10, 10)
        self.game_over_position = (
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2
        )

    def increase_score(self):
        """
        Called when the snake eats food: increments the score counter by 1.
        """
        self.score += 1

    def draw(self, surface):
        """
        Draws the current score onto the given Pygame surface each frame.
        :param surface: The Pygame surface (screen) where text will be blitted.
        """
        score_text = f"Score: {self.score}"
        text_surf = self.font_score.render(score_text, True, self.score_text_color)
        surface.blit(text_surf, self.score_position)

    def draw_game_over(self, surface):
        """
        Draws a "GAME OVER" message and the final score when the game ends.
        :param surface: The Pygame surface (screen) where text will be blitted.
        """
        go_surf = self.font_game_over.render("GAME OVER", True, self.game_over_text_color)
        go_rect = go_surf.get_rect(center=self.game_over_position)
        surface.blit(go_surf, go_rect)

        final_text = f"Final Score: {self.score}"
        final_surf = self.font_score.render(final_text, True, self.score_text_color)

        final_rect = final_surf.get_rect(
            center=(
                self.game_over_position[0],
                self.game_over_position[1] + 50
            )
        )

        surface.blit(final_surf, final_rect)