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
        # bubble sort on a copy to avoid mutating original list
        if not arr:
            return 0
        lst = arr.copy()
        n = len(lst)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    swapped = True
            if not swapped:
                break          # stop if array is already sorted
        return lst[-1]     # highest value ends up at the end

    def draw(self, surface):
        # render and blit live score at top-left
        text = f"Score: {self.score}"
        surf = self.score_font.render(text, True, self.score_color)
        surface.blit(surf, self.score_pos)

    def draw_game_over(self, surface, message="GAME OVER"):
        # draw the main game-over message centered
        self.record_final_score()  # record this game’s score
        surf = self.game_over_font.render(message, True, self.game_over_color)
        rect = surf.get_rect(center=self.game_over_pos)
        surface.blit(surf, rect)

        # show final score below the message
        final = f"Final Score: {self.score}"
        fs = self.score_font.render(final, True, self.score_color)
        offset_final = self.game_over_font.get_height() + 10  # offset based on font height
        fr = fs.get_rect(center=(
            self.game_over_pos[0],
            self.game_over_pos[1] + offset_final
        ))
        surface.blit(fs, fr)

        # show all-time high score below that
        high_value = self.get_first_of_sorted(self.all_scores)
        high_text = f"High Score: {high_value}"
        hs = self.high_score_font.render(high_text, True, self.score_color)
        offset_high = (
            self.game_over_font.get_height() +
            self.high_score_font.get_height() + 20
        )  # further offset below final score
        hr = hs.get_rect(center=(
            self.game_over_pos[0],
            self.game_over_pos[1] + offset_high
        ))
        surface.blit(hs, hr)