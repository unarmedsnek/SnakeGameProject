import pygame
import config


class Button:
    def __init__(self, x, y, width, height, font_size, action, text='', text_color=None, button_color=None,
                 hover_color=None):
        # Store button properties
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle for position and size
        self.text = text  # Text to display on the button
        self.action = action  # Action to perform when clicked (e.g., "START", "QUIT")

        # Font for button text
        self.font = pygame.font.SysFont(config.FONT_NAME, font_size)
        # Text color (default to config BUTTON_TEXT_COLOR if not specified)
        self.text_color = text_color if text_color else config.BUTTON_TEXT_COLOR
        # Optional button background colors
        self.button_color = button_color
        self.hover_color = hover_color

        # Render the text surface
        self.text_surf = self.font.render(self.text, True, self.text_color)
        # Center the text within the button
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Optional: Draw button background if colors are defined
        mouse_pos = pygame.mouse.get_pos()
        if self.button_color:
            current_color = self.button_color
            if self.hover_color and self.rect.collidepoint(mouse_pos):
                current_color = self.hover_color
            pygame.draw.rect(screen, current_color, self.rect, border_radius=5)  # Added border_radius

        # Draw the text on the screen
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        # Check if the given mouse position is within the button's bounds
        return self.rect.collidepoint(mouse_pos)


class MainMenuScreen:
    def __init__(self, scoreboard_instance):
        # Store the scoreboard instance to interact with player data
        self.scoreboard = scoreboard_instance

        # Fonts
        self.title_font = pygame.font.SysFont(config.FONT_NAME, config.TITLE_FONT_SIZE)
        self.input_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_INPUT_TEXT)
        self.player_list_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_PLAYER_LIST)

        # Player Name Input
        self.player_name_input_text = ""
        self.input_rect_width = 300
        self.input_rect_height = 40
        self.input_rect = pygame.Rect(
            (config.SCREEN_WIDTH // 2) - (self.input_rect_width // 2),
            config.SCREEN_HEIGHT // 3 + 60,
            self.input_rect_width,
            self.input_rect_height
        )
        self.input_active = False
        self.placeholder_text = "Enter Player Name"

        # --- MODIFICATION: Store clickable player entry rects ---
        # This list will be populated by the draw method with (name, rect) tuples
        self.clickable_player_entries = []

        # Buttons list
        self.buttons = []

        # Add Player Button
        self.add_player_button = Button(
            self.input_rect.centerx - (150 // 2),
            self.input_rect.bottom + 10,
            150, 40, config.BUTTON_FONT_SIZE,
            'ADD_PLAYER', 'Add Player'
        )
        self.buttons.append(self.add_player_button)

        # Start Button and Quit Button (positioning will be adjusted dynamically)
        # Initial placeholder Y, will be updated in draw()
        self.start_button = Button(
            (config.SCREEN_WIDTH // 2) - (150 // 2),
            0,  # Placeholder Y
            150, 50, config.BUTTON_FONT_SIZE,
            'START', 'Start Game'
        )
        self.buttons.append(self.start_button)

        self.quit_button = Button(
            (config.SCREEN_WIDTH // 2) - (150 // 2),
            0,  # Placeholder Y
            150, 50, config.BUTTON_FONT_SIZE,
            'QUIT', 'Quit'
        )
        self.buttons.append(self.quit_button)

    def draw(self, screen):
        # Background
        # screen.fill(config.BACKGROUND_COLOR)

        # Draw Title
        title_text = 'SNAKE GAME'
        title_surf = self.title_font.render(title_text, True, config.TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4))
        screen.blit(title_surf, title_rect)

        # Draw Player Name Input Field
        input_box_color = config.INPUT_BOX_COLOR_ACTIVE if self.input_active else config.INPUT_BOX_COLOR_INACTIVE
        pygame.draw.rect(screen, input_box_color, self.input_rect, border_radius=5)

        display_text = self.player_name_input_text if self.player_name_input_text else self.placeholder_text
        text_color = config.INPUT_TEXT_COLOR if self.player_name_input_text else config.PLACEHOLDER_TEXT_COLOR

        text_surf = self.input_font.render(display_text, True, text_color)
        text_rect = text_surf.get_rect(centery=self.input_rect.centery, left=self.input_rect.left + 10)
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(screen, config.PLAYER_NAME_COLOR, self.input_rect, 2, border_radius=5)

        # Draw Add Player button (it's part of self.buttons now, drawn below)
        # self.add_player_button.draw(screen) # No, it's drawn in the loop

        # --- MODIFICATION: Draw Player Scores Table and get clickable rects ---
        table_start_x = self.input_rect.left
        table_start_y = self.add_player_button.rect.bottom + 20

        # The draw_player_scores_table now returns a list of (name, rect) and the Y offset after the table
        self.clickable_player_entries, last_y_of_table = self.scoreboard.draw_player_scores_table(
            screen,
            table_start_x,
            table_start_y,
            current_selected_player=self.scoreboard.current_player_name,  # Pass current player for highlighting
            max_players_to_show=5
        )

        # --- Dynamically position Start and Quit buttons below the player list ---
        min_y_for_start_button = last_y_of_table + 20  # Ensure space after the table

        self.start_button.rect.top = min_y_for_start_button
        self.start_button.text_rect.center = self.start_button.rect.center

        self.quit_button.rect.top = self.start_button.rect.bottom + 15
        self.quit_button.text_rect.center = self.quit_button.rect.center

        # --- Draw all buttons (Add Player, Start, Quit) ---
        for button in self.buttons:
            button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                click_pos = event.pos

                # Check if input field was clicked
                if self.input_rect.collidepoint(click_pos):
                    self.input_active = True
                else:
                    self.input_active = False  # Deactivate if clicked outside

                # --- MODIFICATION: Check for clicks on player names in the list ---
                # This should be checked BEFORE buttons, if player list overlaps buttons.
                # Assuming player list is drawn above main action buttons here.
                for name, rect in self.clickable_player_entries:
                    if rect.collidepoint(click_pos):
                        self.scoreboard.set_current_player(name)
                        print(f"Player selected: {name}")
                        # Optionally, clear input field when a player is selected from the list
                        # self.player_name_input_text = ""
                        # self.input_active = False
                        return None  # Consumed event, no further action needed like button press

                # Check if any button was clicked
                for button in self.buttons:
                    if button.is_clicked(click_pos):
                        if button.action == 'ADD_PLAYER':
                            if self.player_name_input_text.strip():
                                added = self.scoreboard.add_player(self.player_name_input_text.strip())
                                if added:
                                    print(f"Player added and selected: {self.scoreboard.current_player_name}")
                                self.player_name_input_text = ""
                                self.input_active = False
                            return None
                        else:
                            return button.action  # START or QUIT

        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                if self.player_name_input_text.strip():
                    added = self.scoreboard.add_player(self.player_name_input_text.strip())
                    if added:
                        print(f"Player added and selected (Enter): {self.scoreboard.current_player_name}")
                    self.player_name_input_text = ""
                self.input_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.player_name_input_text = self.player_name_input_text[:-1]
            else:
                if len(self.player_name_input_text) < 20:
                    self.player_name_input_text += event.unicode

        return None