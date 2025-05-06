from idlelib.colorizer import color_config

import pygame
from scoreboard import Scoreboard
import config

class Button:
    def __init__(self, x, y, width, height, font_size, action, text=''):
        self.font_size = font_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(config.FONT_NAME, font_size)
        self.text_color = config.BUTTON_TEXT_COLOR
        self.action = action

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)


    def draw(self, screen):
        screen.blit(self.text_surf, self.text_rect)


    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class MainMeniuScreen:
    def __init__(self):

        self.title_font = pygame.font.Font(config.FONT_NAME, config.TITLE_FONT_SIZE)
        self.button_font = pygame.font.Font(config.FONT_NAME, config.BUTTON_FONT_SIZE)

        self.buttons = []
        self.start_button = Button(
            (config.SCREEN_WIDTH // 2) - (150 // 2),
            config.SCREEN_HEIGHT / 2,
            150,
            50,
            config.BUTTON_FONT_SIZE,
            'START',
            'Start'
        )
        self.buttons.append(self.start_button)

        self.quit_button = Button(
            (config.SCREEN_WIDTH // 2) - (150 // 2),
            self.start_button.rect.bottom + 15,
            150,
            50,
            config.BUTTON_FONT_SIZE,
            'QUIT',
            'Quit'
        )
        self.buttons.append(self.quit_button)

    def draw(self, screen):

        background_image = pygame.image.load(config.BACKGROUND_IMAGE_START)
        background_image = pygame.transform.scale(background_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))

        title_text = 'SNAKE GAME'
        self.title_surf = self.title_font.render(title_text, True, config.TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect(center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3))

        screen.blit(self.title_surf, self.title_rect)

        for button in self.buttons:
            button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = event.pos
                for button in self.buttons:
                    if button.is_clicked(click_pos):
                        return button.action


class ScoreboardUIScreen:
    def __init__(self, scoreboard):
        self.scoreboard = scoreboard

        if not pygame.font.get_init():
            pygame.font.init()

        self.score_font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE_SCORE)
        self.game_over_font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE_GAMEOVER)
        self.high_score_font = pygame.font.Font(config.FONT_NAME, config.FONT_HIGH_SCORE)

        self.score_color = config.SCORE_TEXT_COLOR
        self.game_over_color = config.GAME_OVER_TEXT_COLOR

        self.score_pos = (10, 10)
        self.game_over_pos = (
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2
        )

        # Button settings
        button_width = 150
        button_height = 50

        self.restartbutton = Button(
            (config.SCREEN_WIDTH // 2) - (button_width // 2),
            (config.SCREEN_HEIGHT // 2) + 150,
            button_width,
            button_height,
            config.BUTTON_FONT_SIZE,
            'RESTART',
            'Restart'
        )

    def draw_score(self, surface):
        text = f"Score: {self.scoreboard.score}"
        surf = self.score_font.render(text, True, self.score_color)
        surface.blit(surf, self.score_pos)

    def draw_game_over(self, surface, message="GAME OVER"):
        self.scoreboard.record_final_score()

        # GAME OVER title
        surf = self.game_over_font.render(message, True, self.game_over_color)
        rect = surf.get_rect(center=self.game_over_pos)
        surface.blit(surf, rect)

        # Final score
        final = f"Final Score: {self.scoreboard.score}"
        fs = self.score_font.render(final, True, self.score_color)
        offset_final = self.game_over_font.get_height() + 10
        fr = fs.get_rect(center=(self.game_over_pos[0], self.game_over_pos[1] + offset_final))
        surface.blit(fs, fr)

        # High score
        high_value = self.scoreboard.get_first_of_sorted(self.scoreboard.all_scores)
        high_text = f"High Score: {high_value}"
        hs = self.high_score_font.render(high_text, True, self.score_color)
        offset_high = self.game_over_font.get_height() + self.high_score_font.get_height() + 20
        hr = hs.get_rect(center=(self.game_over_pos[0], self.game_over_pos[1] + offset_high))
        surface.blit(hs, hr)

        # Draw button
        self.restartbutton.draw(surface)