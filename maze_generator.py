import numpy as np
import random
import pygame  
from sys import exit

class Sugar(pygame.sprite.Sprite):
    def __init__(self, ):
        # TODO: implement x y
        super(Sugar, self).__init__()
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255, 255, 255))
        self.screen_offset = np.array((50, 100))

class Maze:
    """
    Generate a maze See https://en.wikipedia.org/wiki/Maze_generation_algorithm
    Returns either
        a (y, x, 2) size Numpy Array with 0 as a passage and 1 as a wall for the down and right walls of each cell; outer edges are always walls.
        a (y * 2 + 1, x * 2 + 1) size Numpy Array with 0 as a corridor and 1 as a wall block; outer edges are wall blocks.
    """

    def __init__(self, screen=None):

        self.size_x = 10
        self.size_y = 10
        # initialize an array of block data - each passage (0) and wall (1) is a block
        self.block_size = np.array([self.size_y * 2 + 1, self.size_x * 2 + 1], dtype=np.int16)
        self.blocks = np.ones((self.block_size[0], self.block_size[1]), dtype=np.byte)
        self.block_dim = 20  # block size in pixels
        
        self.screen = screen  # if this is set to a display surface, maze generation will be shown in a window
        self.screen_size = self.block_size * self.block_dim
        self.screen_offset = np.array((50, 100))

        self.prev_update = 0
        self.clock = pygame.time.Clock()
        self.slow_mode = False
        # self.slow_mode = True
        self.running = True

        # initialize an array of walls filled with ones, data "not visited" + if exists for 2 walls (down and right) per cell.
        self.wall_size = np.array([self.size_y, self.size_x], dtype=np.int16)
        # add top, bottom, left, and right (ie. + 2 and + 2) to array size so can later work without checking going over its boundaries.
        self.walls = np.ones((self.wall_size[0] + 2, self.wall_size[1] + 2, 3), dtype=np.byte)
        # mark edges as "unusable" (-1)
        self.walls[:, 0, 0] = -1
        self.walls[:, self.wall_size[1] + 1, 0] = -1
        self.walls[0, :, 0] = -1
        self.walls[self.wall_size[0] + 1, :, 0] = -1
    
    def gen_maze_walls_recursive_backtracking(self, corridor_len=5):

        # Generate a maze.
        # This will start with a random cell and create a corridor until corridor length >= corridor_len or it cannot continue the current corridor.
        # Then it will continue from a random point within the current maze (ie. visited cells), creating a junction, until no valid starting points exist.
        # Setting a small corridor maximum length (corridor_len) will cause more branching / junctions.
        # Returns maze walls data - a NumPy array size (y, x, 2) with 0 or 1 for down and right cell walls.

        # set a random starting cell and mark it as "visited"
        cell = np.array([random.randrange(2, self.wall_size[0]), random.randrange(2, self.wall_size[1])], dtype=np.int32)
        self.walls[cell[0], cell[1], 0] = 0

        # a simple definition of the four neighboring cells relative to current cell
        up    = np.array([-1,  0], dtype=np.int32)
        down  = np.array([ 1,  0], dtype=np.int32)
        left  = np.array([ 0, -1], dtype=np.int32)
        right = np.array([ 0,  1], dtype=np.int32)

        # preset some variables
        need_cell_range = False
        round_nr = 0
        corridor_start = 0
        if corridor_len <= 4:
            corridor_len = 5  # even this is too small usually

        while np.size(cell) > 0 and self.running:

            round_nr += 1
            # get the four neighbors for current cell (cell may be an array of cells)
            cell_neighbors = np.vstack((cell + up, cell + left, cell + down, cell + right))
            # valid neighbors are the ones not yet visited
            valid_neighbors = cell_neighbors[self.walls[cell_neighbors[:, 0], cell_neighbors[:, 1], 0] == 1]

            if np.size(valid_neighbors) > 0:
                # there is at least one valid neighbor, pick one of them (at random)
                neighbor = valid_neighbors[random.randrange(0, np.shape(valid_neighbors)[0]), :]
                if np.size(cell) > 2:
                    # if cell is an array of cells, pick one cell with this neighbor only, at random
                    cell = cell[np.sum(abs(cell - neighbor), axis=1) == 1]  # cells where distance to neighbor == 1
                    cell = cell[random.randrange(0, np.shape(cell)[0]), :]
                # mark neighbor visited
                self.walls[neighbor[0], neighbor[1], 0] = 0
                # remove the wall between current cell and neighbor. Applied to down and right walls only so may be that of the cell or the neighbor
                self.walls[min(cell[0], neighbor[0]), min(cell[1], neighbor[1]), 1 + abs(neighbor[1] - cell[1])] = 0
                if self.screen is not None:
                    # if screen is set, draw the corridor from cell to neighbor
                    self.draw_cell(cell, neighbor)
                # check if more corridor length is still available
                if round_nr - corridor_start < corridor_len:
                    # continue current corridor: set current cell to neighbor
                    cell = np.array([neighbor[0], neighbor[1]], dtype=np.int32)
                else:
                    # maximum corridor length fully used; make a new junction and continue from there
                    need_cell_range = True

            else:
                # no valid neighbors for this cell
                if np.size(cell) > 2:
                    # if cell already contains an array of cells, no more valid neighbors are available at all
                    cell = np.zeros((0, 0))  # this will end the while loop, the maze is finished.
                    if self.screen is not None:
                        # if screen is set, make sure it is updated as the maze is now finished.
                        pygame.display.flip()
                else:
                    # a dead end; make a new junction and continue from there
                    need_cell_range = True

            if need_cell_range:
                # get all visited cells (=0) not marked as "no neighbors" (=-1), start a new corridor from one of these (make a junction)
                cell = np.transpose(np.nonzero(self.walls[1:-1, 1:-1, 0] == 0)) + 1  # not checking the edge cells, hence needs the "+ 1"
                # check these for valid neighbors (any adjacent cell with "1" as visited status (ie. not visited) is sufficient, hence MAX)
                valid_neighbor_exists = np.array([self.walls[cell[:, 0] - 1, cell[:, 1], 0],
                                                  self.walls[cell[:, 0] + 1, cell[:, 1], 0],
                                                  self.walls[cell[:, 0], cell[:, 1] - 1, 0],
                                                  self.walls[cell[:, 0], cell[:, 1] + 1, 0]
                                                  ]).max(axis=0)
                # get all visited cells with no neighbors
                cell_no_neighbors = cell[valid_neighbor_exists != 1]
                # mark these (-1 = no neighbors) so they will no longer be actively used. This is not required but helps with large mazes.
                self.walls[cell_no_neighbors[:, 0], cell_no_neighbors[:, 1], 0] = -1
                corridor_start = round_nr + 0  # start a new corridor.
                need_cell_range = False

        # return: drop out the additional edge cells. All cells visited anyway so just return the down and right edge data.
        if self.running:
            return self.walls[1:-1, 1:-1, 1:3]

    def gen_maze_2D(self, corridor_len=5):

        # converts walls data from gen_maze_walls to a NumPy array size (y * 2 + 1, x * 2 + 1)
        # wall blocks are represented by 1 and corridors by 0.

        self.gen_maze_walls_recursive_backtracking(corridor_len)

        if self.running:
            # use wall data to set final output maze
            self.blocks[1:-1:2, 1:-1:2] = 0  # every cell is visited if correctly generated
            # horizontal walls
            self.blocks[1:-1:2, 2:-2:2] = self.walls[1:-1, 1:-2, 2]  # use the right wall
            # vertical walls
            self.blocks[2:-2:2, 1:-1:2] = self.walls[1:-2, 1:-1, 1]  # use the down wall

            return self.blocks
    
    def draw_cell(self, cell, neighbor):

        # draw passage from cell to neighbor. As these are always adjacent can min/max be used.
        min_coord = (np.flip(np.minimum(cell, neighbor) * 2 - 1) * self.block_dim + self.screen_offset).astype(np.int16)
        max_coord = (np.flip(np.maximum(cell, neighbor) * 2 - 1) * self.block_dim + int(self.block_dim) + self.screen_offset).astype(np.int16)
        pygame.draw.rect(self.screen, (255, 255, 0), (min_coord, max_coord - min_coord))

        if self.slow_mode or pygame.time.get_ticks() > self.prev_update + 50:
            self.prev_update = pygame.time.get_ticks()
            pygame.display.flip()

            # when performing display flip, handle some pygame events as well.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

        if self.slow_mode:
            pygame.time.wait(200)


if __name__ == '__main__':

    # Run and display the Maze.
    # Left mouse button or space bar: generate a new maze. 
    # ESC or close the window: Quit.

    # set screen size and initialize it
    pygame.display.init()
    disp_size = (1280, 720)
    rect = np.array([0, 0, disp_size[0], disp_size[1]])  # the rect inside which to draw the maze. Top x, top y, width, height.

    block_dim = 20  # block size in pixels
    screen = pygame.display.set_mode(disp_size)
    pygame.display.set_caption('Ant Game')
    running = True

    while running:
        maze = Maze(screen)
        screen.fill((0, 0, 0))

        # generate the maze - parameter: corridor length (optional)
        start_time = pygame.time.get_ticks()
        print(f'Generating a maze of {maze.wall_size[1]} x {maze.wall_size[0]} = {maze.wall_size[0] * maze.wall_size[1]} cells. Block dimension = {maze.block_dim}.')
        maze.gen_maze_2D()
        if maze.running:
            print('Ready. Time: {:0.4f} seconds.'.format((pygame.time.get_ticks() - start_time) / 1000.0))
            print('ESC or close the Maze window to end program. SPACE BAR for a new maze.')
        else:
            print('Aborted.')
        print(maze.blocks[:,:])

        # wait for exit (window close or ESC key) or left mouse button (new maze) or other key commands
        pygame.event.clear()  # clear the event queue
        running = maze.running
        pausing = maze.running
        while pausing:
            event = pygame.event.wait()  # wait for user input, yielding to other prcesses
            if event.type == pygame.QUIT:
                pausing = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausing = False
                if event.key == pygame.K_ESCAPE:
                    pausing = False
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left button: new maze
                    pausing = False


    # exit; close display
    pygame.quit()
    exit()
