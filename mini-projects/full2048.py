"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048
    """
    tmp_line = merge_padding(line)
    line_index = 0
    while line_index < len(tmp_line) - 1: #loop for merging equal numbers
        first = tmp_line[line_index]
        second = tmp_line[line_index+1]
        if first == second:
            tmp_line[line_index] = first + second
            tmp_line[line_index+1] = 0
            line_index += 2
        if first != second:
            line_index += 1
    return merge_padding(tmp_line)

def merge_padding(line):
    """
    Helper function for merge()
    """
    tmp_line = []
    for elem in line:
        if elem != 0:
            tmp_line.append(elem)
    tmp_line += [0] * (len(line) - len(tmp_line)) # padding with zeros
    return tmp_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._rows = grid_height
        self._columns = grid_width
        self.reset()
        init_tiles_up = [(0, cell) for cell in xrange(grid_width)]
        init_tiles_down = [(grid_height-1, cell) for cell in xrange(grid_width)]
        init_tiles_left = [(cell, 0) for cell in xrange(grid_height)]
        init_tiles_right = [(cell, grid_width-1) for cell in xrange(grid_height)]
        self.init_tiles = {UP: init_tiles_up,
                          DOWN: init_tiles_down,
                          LEFT: init_tiles_left,
                          RIGHT: init_tiles_right}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for col in xrange(self._columns)] \
                    for row in xrange(self._rows)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return '\n'.join([' '.join([str(cell) for cell in self._grid[row]])\
                          for row in xrange(self._rows)])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._rows

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._columns

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # Length of the row or col
        if direction in [UP, DOWN]:
            length = self._rows
        else:
            length = self._columns

        # merging along the given direction
        tile_changed = False
        for init_tile in self.init_tiles[direction]:
            # finding indices and values in that tile
            line_indices = [tuple(sum(x) 
                for x in zip(init_tile, tuple(step * x for x in OFFSETS[direction]))) 
                for step in xrange(length)]
            line_values = [self.get_tile(index[0], index[1])
                               for index in line_indices]
            # Merge the current line
            merged_line = merge(line_values)
            # Replace the original grids with merged result
            for tile in xrange(length):
                row, col = line_indices[tile][0], line_indices[tile][1]
                if self.get_tile(row, col) != merged_line[tile]:
                    tile_changed = True
                self.set_tile(row, col, merged_line[tile])
        if tile_changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_tiles = []
        for row in xrange(len(self._grid)): # list of empty tiles
            for cell in xrange(len(self._grid[row])):
                if self._grid[row][cell] == 0:
                    empty_tiles.append((row, cell))
        weighted_list = [2]*90 + [4]*10 # for selection of 2 or 4
        
        random_cell = random.choice(empty_tiles)
        random_value = random.choice(weighted_list)
        row_num = random_cell[0]
        col_num = random_cell[1]
        # updating grid with new tile
        self.set_tile(row_num, col_num, random_value)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
