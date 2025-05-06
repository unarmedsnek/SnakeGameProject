# Base settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Derived settings (calculated here!)
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors of each element
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_IMAGE = ('snakegame.jpg')
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 0)
SCORE_TEXT_COLOR = (0, 255, 0)
GAME_OVER_TEXT_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (0, 0, 255)
BUTTON_TEXT_COLOR = (255, 0, 0)
TITLE_COLOR = (255, 255, 255)

# Colors for Player UI
PLAYER_NAME_COLOR = (255, 255, 255)  # Color for player names in lists
INPUT_BOX_COLOR_INACTIVE = (100, 100, 100) # Color for the player name input box when inactive
INPUT_BOX_COLOR_ACTIVE = (150, 150, 150) # Color for the player name input box when active
INPUT_TEXT_COLOR = (255, 255, 255) # Color for the text typed into the input box
PLACEHOLDER_TEXT_COLOR = (200, 200, 200) # Color for placeholder text in input box

# Color for highlighting the currently selected player in lists
SELECTED_PLAYER_HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow

# Gameplay
GAME_SPEED = 10

# FONTS
FONT_NAME = None

# Font sizes
FONT_SIZE_SCORE = 24
FONT_SIZE_GAMEOVER = 48
FONT_HIGH_SCORE = 24
BUTTON_FONT_SIZE = 24
TITLE_FONT_SIZE = 48

# Font sizes for Player UI
FONT_SIZE_PLAYER_LIST = 20 # Font size for the player list/scoreboard table
FONT_SIZE_INPUT_TEXT = 22 # Font size for the text input field

#BACKGROUND_COLOR = (0, 0, 0)