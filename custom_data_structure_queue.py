#Mohammad Badri
class SnakeBodyData:
    # How to call the function snake_body = SnakeBodyData()
    #for better understanding I used the name "Nodes" instead of segments so Nodes = segments it's the snake body parts
    '''
    Custom data structure to efficiently manage snake body
    '''
    def __init__(self):
        self._segments = []
        '''
        Empty snake body
        This function hold all the (x,y) position of the snake body, representing a coordinate on the grid.
        Head is the index 0 and Tail is the index -1.  self._segments[index]
        '''

    def add_first(self, segments):
        '''
        adds a new segment at the front of the snake, represent the new head position
        example:
        we have a snake with this postion segments [(5,5),(5,6),(5,7)]
        Head is (5,5)
        next body part is (5,6)
        Tail is (5,7)
        If the user press the left bottom then snake moves to left:
        The function add_first is called with new segment add_first(4,5)
        the new snake will be [(4,5),(5,5),(5,6),(5,7)] but after adding we also need to remove from the tail, this happen if snake ate an apple if not then the remove function is called
        remove.last will remove the tail (5,7).
        '''
        self._segments.insert(0,segments)

    def remove_last(self):
        '''
        Removes and returns the last segment of the snake (the tail).

        Returns:
        tuple or None: The removed tail segment (x, y) or None if the snake has no segments.
        '''
        if self._segments:
            return self._segments.pop()
        return None

    def get_first(self):
        '''
        returns the postion of the Head for example (4,5) index 0 in the tuple
        needed for calculation next position, collision to wall or it's self,
        Returns:
        tuple or None: The head segment (x, y) or None if the snake has no segments.
        '''
        return self._segments[0] if self._segments else None

    def get_all_segments(self):
        '''
        return entire snake body.
        we use list to return a copy of the list, the actual list is protected and cant be changed.
        the rendering loop will draw the snake segments using the list
        it will also be used to check for any collision, if the snake touches(overlap) itself.


        returns: A list of coordinates (x,y) representing the snake body
        '''
        return list(self._segments)
    def __contains__(self, item):
        '''
        Checks if a segment is in the snake's body.
        arg:
        Tuple: The coordinates to check
        returns:
        bool: True if the item is in the snake's body.
        example usage:
        snake = SnakeBodyData()
        snake.add_first((5, 5))
        print((5, 5) in snake)
        '''
        return item in self._segments
    def __len__(self):
        '''
        returns the number of segments in the snake's body the length of the snake

        example:
        snake_body = SnakeBodyData()
        print(len(snake_body))
        -----------------------------
        snake_body._segments = [(5, 5), (5, 6), (5, 7)]
        print(len(snake_body))  output 3
        '''
        return len(self._segments)







