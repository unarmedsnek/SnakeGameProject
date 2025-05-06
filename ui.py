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
        self.font = pygame.font.SysFont(config.FONT_NAME, font_size)
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

        self.title_font = pygame.font.SysFont(config.FONT_NAME, config.TITLE_FONT_SIZE)
        self.button_font = pygame.font.SysFont(config.FONT_NAME, config.BUTTON_FONT_SIZE)

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