# Abd Alah Fashesh

import pygame
import config

class Scoreboard:
    def __init__(self):
        self.score = 0           # current game score
        self.all_scores = []     # history of past final scores

        # ensure font module is ready before creating fonts
        if not pygame.font.get_init():
            pygame.font.init()

        # fonts for different displays
        self.score_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_SCORE
        )
        self.game_over_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_GAMEOVER
        )
        self.high_score_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_HIGH_SCORE
        )

        # text colors from config
        self.score_color = config.SCORE_TEXT_COLOR
        self.game_over_color = config.GAME_OVER_TEXT_COLOR

        # positions: live score in top-left, game-over centered
        self.score_pos = (10, 10)
        self.game_over_pos = (
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2
        )

    def reset(self):
        self.score = 0           # reset score for a new game

    def increase_score(self):
        self.score += 1          # called when snake eats; bump score

    def record_final_score(self):
        self.all_scores.append(self.score)  # save final score to history

    def get_first_of_sorted(self, arr):
        #bubble
        if not arr:
            return 0
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break          # stop if array is already sorted
        return arr[-1]     # highest value ends up at the end

    def draw(self, surface):
        # render and blit live score at top-left
        text = f"Score: {self.score}"
        surf = self.score_font.render(text, True, self.score_color)
        surface.blit(surf, self.score_pos)

    def draw_game_over(self, surface, message="GAME OVER"):
        # draw the main game-over message centered
        surf = self.game_over_font.render(message, True, self.game_over_color)
        rect = surf.get_rect(center=self.game_over_pos)
        surface.blit(surf, rect)

        # show final score below the message
        final = f"Final Score: {self.score}"
        fs = self.score_font.render(final, True, self.score_color)
        fr = fs.get_rect(center=(
            self.game_over_pos[0],
            self.game_over_pos[1] + config.FONT_SIZE_GAMEOVER + 10  # offset dynamically
        ))
        surface.blit(fs, fr)

        # show all-time high score below that
        high_value = self.get_first_of_sorted(self.all_scores)
        high_text = f"High Score: {high_value}"
        hs = self.high_score_font.render(high_text, True, self.score_color)
        hr = hs.get_rect(center=(
            self.game_over_pos[0],
            self.game_over_pos[1] + config.FONT_SIZE_GAMEOVER + config.FONT_HIGH_SCORE + 20
        ))
        surface.blit(hs, hr)
