# Abd Alah Fashesh

import pygame
import config

class Scoreboard:
    """
    Manages and displays the game score and game over message.
    """
    def __init__(self):
        # start score and history
        self.score = 0
        self.all_scores = []

        # init font system if needed
        if not pygame.font.get_init():
            pygame.font.init()

        # set up fonts
        self.font_score = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SCORE)
        self.font_game_over = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_GAMEOVER)

        # text colors
        self.score_color = config.SCORE_TEXT_COLOR
        self.game_over_color = config.GAME_OVER_TEXT_COLOR

        # positions
        self.score_pos = (10, 10)
        cx = config.SCREEN_WIDTH // 2
        cy = config.SCREEN_HEIGHT // 2
        self.game_over_pos = (cx, cy)

    def reset(self):
        """Reset score for a new game."""
        self.score = 0

    def increase_score(self):
        """Called when the snake eats: increment score."""
        self.score += 1

    def record_final_score(self):
        """Store the final score in history."""
        self.all_scores.append(self.score)

    def get_high_score(self):
        """Return the highest score seen so far."""
        if self.all_scores:
            return max(self.all_scores)
        return 0

    def draw(self, surface):
        """Draw the live score in the top-left corner."""
        text = f"Score: {self.score}"
        surf = self.font_score.render(text, True, self.score_color)
        surface.blit(surf, self.score_pos)

    def draw_game_over(self, surface, message="GAME OVER"):
        """Draw game-over text, final score, and high score."""
        # main message
        go_s = self.font_game_over.render(message, True, self.game_over_color)
        go_r = go_s.get_rect(center=self.game_over_pos)
        surface.blit(go_s, go_r)

        # final score below
        final = f"Final Score: {self.score}"
        f_s = self.font_score.render(final, True, self.score_color)
        f_r = f_s.get_rect(center=(self.game_over_pos[0], self.game_over_pos[1] + 40))
        surface.blit(f_s, f_r)

        # high score below that
        high = self.get_high_score()
        if high:
            hs = f"High Score: {high}"
            h_s = self.font_score.render(hs, True, self.score_color)
            h_r = h_s.get_rect(center=(self.game_over_pos[0], self.game_over_pos[1] + 80))
            surface.blit(h_s, h_r)
