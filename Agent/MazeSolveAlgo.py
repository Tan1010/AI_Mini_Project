""" Adapted from https://github.com/john-science/mazelib """

import abc

import numpy as np
from numpy.random import shuffle
from game_constants import Direction

class MazeSolveAlgo:
    """
    0: path, 1: wall, 2: home, 3: sugar, 4: ant, 5: visited
    visited cells:- the cells that have been visited and have no value to be visited again
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.level = 0

    def solve(self, game):
        self.sugar_hold = game.sugar_hold
        self.grid = game.maze.blocks.copy()
        start_pos = np.where(self.grid==4)
        self.start = start_pos[0].item(), start_pos[1].item()
        self.grid[start_pos] = 0
        # Reset visited cells if new/next level
        if self.level != game.level:
            self.visited = np.zeros_like(self.grid, dtype=np.uint8) 
            self.level += 1
        # Update visited cells to the maze grid
        self.grid += self.visited
        # Solve 
        solution_coor = self._solve()
        # Return list of directions 
        direction_np = np.diff(np.array(solution_coor, dtype=np.int8), axis=0)
        directions = [Direction._value2member_map_[x] for x in map(tuple, direction_np)]
        return directions
    
    @abc.abstractmethod
    def _solve(self):
        return None

    def _find_unblocked_neighbors(self, pos):
        """
        Assume ant has vision of its neighbors only 
        Returns:
            list: all the unblocked neighbors to this cell
        """
        y, x = pos
        unblocked_neighbours = []
        sugar_neighbours = []
        home_nearby = False
        for direction in Direction._member_map_.values():
            dy, dx = direction.value
            neighbour_y, neighbour_x = y+dy, x+dx
            neighbour = self.grid[neighbour_y][neighbour_x]
            if neighbour == 2:
                if self.sugar_hold == 2 or not 3 in self.grid:
                    return [(neighbour_y, neighbour_x)]
                home_nearby = True
            if neighbour == 3:
                sugar_neighbours.append((neighbour_y, neighbour_x))
            if neighbour == 0:
                unblocked_neighbours.append((neighbour_y, neighbour_x))

        # mark cells that are visited and at death end
        if (len(sugar_neighbours) + len(unblocked_neighbours) + home_nearby) == 1:
            self.grid[y][x] = 5
            self.visited[y][x] = 5

        shuffle(sugar_neighbours)
        shuffle(unblocked_neighbours)
        
        # if hold 2 sugars, avoid sugar 
        # if hold less than 2 sugars, prioritise sugar 
        return sugar_neighbours if sugar_neighbours and self.sugar_hold != 2 else unblocked_neighbours
    
    def _within_target(self, cell):
        """
        Returns:
            bool: Are you within one movement of your target?
        """
        if not cell:
            return False
        if self.sugar_hold == 2 or not 3 in self.grid:
            return self.grid[cell[0]][cell[1]] == 2
        return self.grid[cell[0]][cell[1]] == 3

