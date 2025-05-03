#Mohammad Badri
from custom_data_structure_queue import SnakeBodyData
from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, SNAKE_COLOR  # Assuming these are in config.py

class Snake:
    """Represents the snake in the game."""

    def __init__(self, initial_position):
        """Initializes the snake.

        Args:
            initial_position (tuple): The starting coordinate (x, y) of the snake's head.
        """
        self._body = SnakeBodyData()
        self._body.add_first(initial_position)
        self._direction = (1, 0)  # Initial direction: right
        self._can_change_direction = True # Flag to prevent immediate 180-degree turns
        self._grow_next_move = False

    def move(self):
        """Moves the snake in its current direction.

        If the snake is set to grow, the tail is not removed.
        """
        head_x, head_y = self._body.get_first()
        dx, dy = self._direction
        new_head = (head_x + dx, head_y + dy)
        self._body.add_first(new_head)
        self._can_change_direction = True  # Reset the flag after a move
        if not self._grow_next_move:
            self._body.remove_last()
        else:
            self._grow_next_move = False

    def grow(self):
        """Sets a flag to make the snake grow on the next move."""
        self._grow_next_move = True

    def change_direction(self, new_direction):
        """Changes the snake's movement direction, preventing 180-degree turns.

        Args:
            new_direction (tuple): A tuple (dx, dy) representing the new direction
                                   (-1, 0): left, (1, 0): right, (0, -1): up, (0, 1): down.
        """
        if not self._can_change_direction:
            return  # Prevent changing direction multiple times in one step

        current_dx, current_dy = self._direction
        new_dx, new_dy = new_direction

        # Prevent 180-degree turns
        if (current_dx == -new_dx and current_dy == -new_dy):
            return

        self._direction = new_direction
        self._can_change_direction = False

    def check_collision_with_self(self):
        """Checks if the snake's head has collided with its own body.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        head = self._body.get_first()
        body = self._body.get_all_segments()[1:]  # Exclude the head
        return head in body

    def get_head_position(self):
        """Returns the current position of the snake's head.

        Returns:
            tuple: The coordinate (x, y) of the head.
        """
        return self._body.get_first()

    def get_body_segments(self):
        """Returns a list of all the snake's body segments.

        Returns:
            list: A list of coordinate tuples (x, y) representing the snake's body.
        """
        return self._body.get_all_segments()

    def draw(self, surface):
        """Draws the snake on the given Pygame surface.

        Args:
            surface (pygame.Surface): The Pygame surface to draw on.
        """
        for segment in self._body.get_all_segments():
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            pygame.draw.rect(surface, SNAKE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

# --- Interface for Member 1 ---
# Member 1 will primarily interact with the Snake class by:
#
# 1. Creating an instance of the Snake class, providing an initial position:
#    my_snake = Snake(initial_position=(5, 5))
#
# 2. Getting the snake's head position:
#    head_pos = my_snake.get_head_position()
#
# 3. Getting all body segments for drawing or collision checks:
#    segments = my_snake.get_body_segments()
#
# 4. Moving the snake:
#    my_snake.move()
#
# 5. Making the snake grow:
#    my_snake.grow()
#
# 6. Changing the snake's direction:
#    my_snake.change_direction((0, 1)) # Example: move down
#
# 7. Checking for self-collision:
#    if my_snake.check_collision_with_self():
#        print("Game Over - Self Collision!")
#
# 8. Drawing the snake on the game screen (Member 2 will likely handle the Pygame setup and loop):
#    # Assuming 'game_surface' is a Pygame Surface created elsewhere
#    # my_snake.draw(game_surface)