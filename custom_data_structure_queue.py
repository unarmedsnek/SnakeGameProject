#Mohammad Badri
class SnakeBodyData:
    """
    Custom data structure to efficiently manage the snake's body segments.
    Uses a Python list internally.
    """
    def __init__(self):
        """Initializes an empty snake body."""
        self._segments = []

    def add_first(self, segment):
        """Adds a new segment to the head of the snake.

        Args:
            segment (tuple): A coordinate tuple (x, y) representing the new head segment.
        """
        self._segments.insert(0, segment)

    def remove_last(self):
        """Removes and returns the last segment of the snake (the tail).

        Returns:
            tuple or None: The removed tail segment (x, y) or None if the snake has no segments.
        """
        if self._segments:
            return self._segments.pop()
        return None

    def get_first(self):
        """Returns the head segment of the snake.

        Returns:
            tuple or None: The head segment (x, y) or None if the snake has no segments.
        """
        return self._segments[0] if self._segments else None

    def get_all_segments(self):
        """Returns a list of all body segments.

        Returns:
            list: A list of coordinate tuples (x, y) representing the snake's body.
        """
        return list(self._segments)  # Return a copy to prevent external modification

    def __len__(self):
        """Returns the current number of segments in the snake's body.

        Returns:
            int: The length of the snake.
        """
        return len(self._segments)