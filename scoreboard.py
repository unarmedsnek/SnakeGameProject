# Replace the entire content of SnakeGameProject/scoreboard.py with the following:

import pygame
import config


class Scoreboard:
    def __init__(self):
        # Current game score for the active player
        self.score = 0
        # Stores all player names and their highest score for the current session
        # Format: { "playerName1": score1, "playerName2": score2 }
        self.players = {}
        # Name of the player currently playing or last added/selected
        self.current_player_name = None
        # History of all scores in the session (can be used for a general high score if needed)
        self.all_scores_history = []

        # Ensure font module is ready
        if not pygame.font.get_init():
            pygame.font.init()

        # Font for the live score display during gameplay
        self.score_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_SCORE
        )
        # Font for "GAME OVER" and related messages
        self.game_over_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_GAMEOVER
        )
        # Font for displaying individual player scores in tables
        self.player_list_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_SIZE_PLAYER_LIST
        )
        # Font for high score display
        self.high_score_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.FONT_HIGH_SCORE
        )

        # Colors from config
        self.score_color = config.SCORE_TEXT_COLOR
        self.game_over_color = config.GAME_OVER_TEXT_COLOR
        self.player_name_color = config.PLAYER_NAME_COLOR

        # Positioning for live score
        self.score_pos = (10, 10)
        # Base position for game over messages
        self.game_over_base_pos = (
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 3  # Adjusted Y to make space for player score table
        )

    def add_player(self, name):
        """Adds a new player if the name is valid and not already taken."""
        # Add player if name is not empty and not already in players
        if name and name not in self.players:
            # Store player with an initial score of 0
            self.players[name] = 0
            # Set the newly added player as the current player
            self.current_player_name = name
            # Return True indicating player was added
            return True
        # Return False if player was not added (e.g., name empty or taken)
        return False

    def set_current_player(self, name):
        """Sets the current player if the name exists in the player list."""
        # Check if the player name exists in our records
        if name in self.players:
            # Set this player as the one whose score will be tracked
            self.current_player_name = name

    def reset_current_game_score(self):
        """Resets the score for the beginning of a new game."""
        # Reset the live score counter to 0
        self.score = 0

    def increase_score(self):
        """Increases the current player's score by 1 (e.g., when food is eaten)."""
        # Increment the live score
        self.score += 1

    def record_final_score(self):
        """Records the final score for the current player at the end of a game."""
        # Check if there is a current player and they are in our player list
        if self.current_player_name and self.current_player_name in self.players:
            # Update the player's score only if the new score is higher than their previous best in this session
            if self.score > self.players[self.current_player_name]:
                self.players[self.current_player_name] = self.score
        # Add the score to the general history (for overall high score if needed)
        self.all_scores_history.append(self.score)

    def get_overall_high_score(self):
        """Calculates the highest score achieved by any player in the session."""
        # Return 0 if no scores have been recorded yet
        if not self.all_scores_history:
            return 0
        # Return the maximum score from the history
        return max(self.all_scores_history)

    def get_ranked_players(self):
        """Returns a list of (name, score) tuples, sorted by score in descending order."""
        # Convert the players dictionary to a list of items (name, score)
        player_data = list(self.players.items())
        # Sort the list: primary key is score (descending), secondary key is name (ascending) for tie-breaking
        sorted_players = sorted(player_data, key=lambda item: (-item[1], item[0]))
        # Return the sorted list
        return sorted_players

    def draw_live_score(self, surface):
        """Draws the current game's score on the screen during gameplay."""
        # Create the text string for the score
        text = f"Score: {self.score}"
        # If a player is active, show their name too
        if self.current_player_name:
            text = f"Player: {self.current_player_name} - Score: {self.score}"
        # Render the text
        score_surf = self.score_font.render(text, True, self.score_color)
        # Blit the score to its designated position
        surface.blit(score_surf, self.score_pos)

    def draw_player_scores_table(self, surface, start_x, start_y, current_selected_player=None, max_players_to_show=10):
        """
        Draws a table of players and their scores, ranked.
        Highlights the current_selected_player.
        Returns a list of (name, rect) for each drawn player entry.
        """
        # Get the ranked list of players
        ranked_players = self.get_ranked_players()
        # List to store information about drawn player entries (name and their rectangle area)
        drawn_player_entries_info = []

        # Title for the table
        title_text = "Player Scores (Click to Select):"  # Updated title to indicate clickability
        title_surf = self.player_list_font.render(title_text, True, self.player_name_color)
        title_rect = title_surf.get_rect(topleft=(start_x, start_y))
        surface.blit(title_surf, title_rect)

        # Vertical offset for each player entry
        line_height = self.player_list_font.get_linesize()
        current_y = start_y + line_height  # Start drawing player names below the title

        # Iterate through ranked players and draw their info
        for i, (name, score) in enumerate(ranked_players[:max_players_to_show]):  # Show top N players
            # Format the player rank, name, and score
            player_text = f"{i + 1}. {name}: {score}"

            # Determine text color: highlight if current_selected_player matches this name
            text_color = config.PLAYER_NAME_COLOR
            if name == current_selected_player:
                text_color = config.SELECTED_PLAYER_HIGHLIGHT_COLOR  # Use highlight color

            # Render the player text
            player_surf = self.player_list_font.render(player_text, True, text_color)
            player_rect = player_surf.get_rect(topleft=(start_x, current_y))
            surface.blit(player_surf, player_rect)

            # Store the name and the rectangle of this player entry for click detection
            drawn_player_entries_info.append((name, player_rect))

            # Move to the next line
            current_y += line_height

        # Return the list of (name, rect) and the y-coordinate after the last drawn item
        return drawn_player_entries_info, current_y

    def draw_game_over_screen(self, surface):
        """Draws the complete game over screen, including scores and player rankings."""
        # Record the final score for the current player
        self.record_final_score()

        # --- Display "GAME OVER" message ---
        game_over_text_surf = self.game_over_font.render("GAME OVER", True, self.game_over_color)
        game_over_text_rect = game_over_text_surf.get_rect(center=self.game_over_base_pos)
        surface.blit(game_over_text_surf, game_over_text_rect)
        current_y_offset = game_over_text_rect.bottom + 20  # Start drawing below "GAME OVER"

        # --- Display current player's final score ---
        if self.current_player_name:
            final_score_text = f"{self.current_player_name}'s Score: {self.score}"
        else:
            final_score_text = f"Final Score: {self.score}"
        final_score_surf = self.score_font.render(final_score_text, True, self.score_color)
        final_score_rect = final_score_surf.get_rect(center=(self.game_over_base_pos[0], current_y_offset))
        surface.blit(final_score_surf, final_score_rect)
        current_y_offset = final_score_rect.bottom + 10

        # --- Display overall session high score ---
        overall_high = self.get_overall_high_score()
        high_score_text = f"Session High Score: {overall_high}"
        high_score_surf = self.high_score_font.render(high_score_text, True, self.score_color)
        high_score_rect = high_score_surf.get_rect(center=(self.game_over_base_pos[0], current_y_offset))
        surface.blit(high_score_surf, high_score_rect)
        current_y_offset = high_score_rect.bottom + 30  # Add more space before the table

        # --- Display ranked player scores table ---
        # Position the table; you might want to adjust X if game_over_base_pos[0] isn't ideal for a left-aligned table
        table_start_x = config.SCREEN_WIDTH // 2 - 150  # Example: Center the table somewhat
        if table_start_x < 20: table_start_x = 20  # Ensure it's not too far left

        self.draw_player_scores_table(surface, table_start_x, current_y_offset)