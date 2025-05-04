#Mohammad Badri
import pygame

import config
from custom_data_structure_queue import SnakeBodyData
from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT

class Snake:
    ''''
    Represent the snake in the game
    initial position for the snake head (x,y)
    initial movement direction

    '''
    def __init__(self,initial_position):
        '''

        '''
        self._body = SnakeBodyData() #creats an instance of custom body manager class, stores all segments of snake
        self._body.add_first(initial_position) #sdding the first segment for example (5,5)
        self._direction = (1, 0)  #initial direction starts from right
        self._can_change_direction = True #prevents the user to make 180-degree turns in the sane frame, it will be reset after each move
        self._grow_next_move = False #if the snake eats the apple it will be set to True
        self._alive = True  #Tracks if the snake is alive or dead

    def move(self):
        '''
        Moves the snake in its current direction
        If the snake is set to grow tail is not removed
        it adds a new head at the next cell (removes each node (part of snake body) and change to the next position in the map)
        it reset the direction lock to allow changing direction
        '''
        head_x, head_y = self._body.get_first() #gets the current head position for example (5,5)
        dx, dy = self._direction
        new_head = (head_x + dx, head_y + dy)
        #Calculates the next head position for example
        '''
        if direction = (1,0) and head = (5,5) -> new head = (6,5)
        '''
        self._body.add_first(new_head) #adds new head to the front of the body
        self._can_change_direction = True #after the snake moves, you allow the direction to be changed again/ prevents player to do two quick turns
        if not self._grow_next_move:#checks if the snake didn't eat the apple then removes the tail so the length stays the same, but if eated tit will skip the removal part            self._body.remove_last()
            self._body.remove_last()
        else:
            self._grow_next_move = False


        '''
        example:
        snake Body: [(5,5),(4,5),(3,5)]
        Direction: (1,0)
        After the move():
        Adds new head (6,5) -> [(6,5)(5,5),(4,5),(3,5)]
        remove last(if snake did not eat the apple) -> [(6,5)(5,5),(4,5)]
        '''

    def grow(self):
        self._grow_next_move = True
        #when the snake ate the apple we will change flag to True so in the next move we don't remove the tail

    def change_direction(self, new_direction):
        if not self._can_change_direction:
            return #prevents changing direction multiple time in one step
        current_dx, current_dy = self._direction
        new_dx, new_dy = new_direction
        if current_dx == -new_dx and current_dy == -new_dy: #need to be checked
            return#prevents 180-degree
        self._direction = new_direction
        self._can_change_direction = False #locks direction change until the snake moves(which will be resets the flag in move())


    def check_collision_with_self(self):
        head = self._body.get_first() #gets the position of the snake's head
        body = self._body.get_all_segments()[1:] #exclude the head, rest of the body
        if head in body:#checks if heads position matches any body segments
            self._alive = False #snake has collided with itself
            return True
        return False


    def is_alive(self):
        return self._alive



    def get_head_position(self):
        '''
        returns the head position of the snake's head
        '''
        return self._body.get_first()

    def check_collision_with_wall(self):
        '''
        gets the head position, checks if it's outside the wall
        less than 0 -> outside the top or left
        greater than or equal to GRIDE_WIDTH or GRIDE_HEIGHT ->outside the right or bottom
        '''
        head_x, head_y = self.get_head_position()
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            self._alive = False
            return True
        return False

    def get_body_segments(self):
        return self._body.get_all_segments()
        #takes the body segment position in a tuple list(copy)

    def draw(self,surface):
        '''
        Draws the snake on the surface
        loops through all body segments of the snake
        draws a rectangle for each segments
        '''
        for segment in self._body.get_all_segments():
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            pygame.draw.rect(surface, config.SNAKE_COLOR, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))


