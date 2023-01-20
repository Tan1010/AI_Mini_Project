import numpy as np
import random
import pygame  
from PIL import Image
from sys import exit

"""
# class Cell(pygame.sprite.Sprite):
#     cell_dim = 20

#     def __init__(self, x, y, offset_x, offset_y):
#         pygame.sprite.Sprite.__init__(self)

#         self.image = pygame.Surface([self.cell_dim, self.cell_dim])
#         self.image.fill((255, 255, 255))
#         self.rect = self.image.get_rect()
#         self.rect.x = x * self.cell_dim + offset_x
#         self.rect.y = y * self.cell_dim + offset_y
#         self.x = x
#         self.y = y

#     def draw(self, screen):
#         screen.blit(self.image, self.rect)


# class Wall(Cell):
#     def __init__(self, x, y, offset_x, offset_y):
#         super(Wall, self).__init__(x, y, offset_x, offset_y)
#         self.image.fill((255, 0, 0))


# class Sugar(pygame.sprite.Sprite):
#     def __init__(self, x, y, offset_x, offset_y):
#         # TODO: implement x y
#         super(Sugar, self).__init__(x, y, offset_x, offset_y)
#         self.surface.fill((0, 255, 255))
"""

class Maze:
    def __init__(self, screen=None):
        self.screen = screen  
        self.size_x = 10
        self.size_y = 10
        self.offset_x = 50
        self.offset_y = 100

        # initialize an array of block data - each passage (0) and wall (1) is a block
        self.block_size = np.array([self.size_y * 2 + 1, self.size_x * 2 + 1], dtype=np.int16)
        self.blocks = np.ones((self.block_size[0], self.block_size[1]), dtype=np.byte)

        # initialize an array of walls filled with ones, data "not visited" + if exists for 2 walls (down and right) per cell.
        self.wall_size = np.array([self.size_y, self.size_x], dtype=np.int16)
        # add top, bottom, left, and right (ie. + 2 and + 2) to array size so can later work without checking going over its boundaries.
        self.walls = np.ones((self.wall_size[0] + 2, self.wall_size[1] + 2, 3), dtype=np.byte)
        # mark edges as "unusable" (-1)
        self.walls[:, 0, 0] = -1
        self.walls[:, self.wall_size[1] + 1, 0] = -1
        self.walls[0, :, 0] = -1
        self.walls[self.wall_size[0] + 1, :, 0] = -1
    
    def gen_maze_walls_recursive_backtracking(self):

        # Generate a maze.
        # This will start with a random cell and create a corridor until corridor length >= corridor_len or it cannot continue the current corridor.
        # Then it will continue from a random point within the current maze (ie. visited cells), creating a junction, until no valid starting points exist.
        # Setting a small corridor maximum length (corridor_len) will cause more branching / junctions.
        # Returns maze walls data - a NumPy array size (y, x, 2) with 0 or 1 for down and right cell walls.

        # set a random starting cell and mark it as "visited"
        cell = np.array([random.randrange(2, self.wall_size[0]), random.randrange(2, self.wall_size[1])], dtype=np.byte)
        self.walls[cell[0], cell[1], 0] = 0

        # a simple definition of the four neighboring cells relative to current cell
        up    = np.array([-1,  0], dtype=np.byte)
        down  = np.array([ 1,  0], dtype=np.byte)
        left  = np.array([ 0, -1], dtype=np.byte)
        right = np.array([ 0,  1], dtype=np.byte)


        while np.size(cell) > 0:
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
                # set current cell to neighbor
                cell = np.array([neighbor[0], neighbor[1]], dtype=np.int32)

            else:
                # no valid neighbors for this cell
                if np.size(cell) > 2:
                    # if cell already contains an array of cells, no more valid neighbors are available at all
                    cell = np.zeros((0, 0))  # this will end the while loop, the maze is finished.
                    # if self.screen is not None:
                    #     # if screen is set, make sure it is updated as the maze is now finished.
                    #     pygame.display.flip()
                else:
                    # a dead end; make a new junction and continue from there
                    # get all visited cells (=0) not marked as "no neighbors" (=-1), start a new corridor from one of these (make a junction)
                    cell = np.transpose(np.nonzero(self.walls[1:-1, 1:-1, 0] == 0)) + 1  # not checking the edge cells, hence needs the "+ 1"
                    # check these for valid neighbors (any adjacent cell with "1" as visited status (ie. not visited) is sufficient, hence MAX)
                    valid_neighbor_exists = np.array([
                        self.walls[cell[:, 0] - 1, cell[:, 1], 0],
                        self.walls[cell[:, 0] + 1, cell[:, 1], 0],
                        self.walls[cell[:, 0], cell[:, 1] - 1, 0],
                        self.walls[cell[:, 0], cell[:, 1] + 1, 0]
                    ]).max(axis=0)
                    # get all visited cells with no neighbors
                    cell_no_neighbors = cell[valid_neighbor_exists != 1]
                    # mark these (-1 = no neighbors) so they will no longer be actively used. This is not required but helps with large mazes.
                    self.walls[cell_no_neighbors[:, 0], cell_no_neighbors[:, 1], 0] = -1

        # return: drop out the additional edge cells. All cells visited anyway so just return the down and right edge data.
        return self.walls[1:-1, 1:-1, 1:3]

    def gen_maze_2D(self):

        # converts walls data from gen_maze_walls to a NumPy array size (y * 2 + 1, x * 2 + 1)
        # wall blocks are represented by 1 and corridors by 0.

        self.gen_maze_walls_recursive_backtracking()

        # use wall data to set final output maze
        self.blocks[1:-1:2, 1:-1:2] = 0  # every cell is visited if correctly generated
        # horizontal walls
        self.blocks[1:-1:2, 2:-2:2] = self.walls[1:-1, 1:-2, 2]  # use the right wall
        # vertical walls
        self.blocks[2:-2:2, 1:-1:2] = self.walls[1:-2, 1:-1, 1]  # use the down wall
        
        # generate home and ant startpoint
        self.blocks[1, 0] = 2   # home
        self.blocks[1, 1] = 10  # ant startpoint

        # generate sugars
        flatten = self.blocks.reshape(-1)
        flatten[np.random.choice(np.where(flatten == 0)[0], 20)] = 3  # replace 20 path cell with sugars
        return self.blocks

    def draw_maze(self):
        BLOCK_DIM = 20
        WALL_COLOR = np.array((48,19,1), dtype=np.uint8)
        ANT_COLOR = np.array((255,0,0), dtype=np.uint8)
        SUGAR_IMG_ARR = np.array(Image.open('Assets\sugar.jpg').convert('RGB'))
        HOME_IMG_ARR = np.array(Image.open('Assets\home.jpg').convert('RGB'))

        # Wall
        self.surface_arr = np.zeros((*tuple(self.block_size), 3), dtype=np.int16) + 255
        self.surface_arr[self.blocks==1] = WALL_COLOR
        self.surface_arr = self.surface_arr.repeat(BLOCK_DIM, axis=0).repeat(BLOCK_DIM, axis=1)

        # Home and ant
        self.surface_arr[20:40, :20] = HOME_IMG_ARR
        self.surface_arr[20:40, 20:40] = ANT_COLOR

        # Sugar
        arr_x_sugar, arr_y_sugar = np.where(self.blocks==3)
        arr_x_sugar, arr_y_sugar = arr_x_sugar*20, arr_y_sugar*20        
        for x, y in zip(arr_x_sugar, arr_y_sugar):
            self.surface_arr[x:x+20, y:y+20] = SUGAR_IMG_ARR

        self.surface = pygame.surfarray.make_surface(np.transpose(self.surface_arr, [1,0,2]))
        self.screen.blit(self.surface, (self.offset_x, self.offset_y))
        # pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':

    # Run and display the Maze.
    # Left mouse button or space bar: generate a new maze. 
    # ESC or close the window: Quit.

    # set screen size and initialize it
    pygame.display.init()

    # Setup the clock for a decent framerate TODO
    clock = pygame.time.Clock()

    block_dim = 20  # block size in pixels
    disp_size = (1280, 720)
    # rect = np.array([0, 0, disp_size[0], disp_size[1]])  # the rect inside which to draw the maze. Top x, top y, width, height.
    screen = pygame.display.set_mode(disp_size)
    pygame.display.set_caption('Ant Game')
    running = True

    while running:
        maze = Maze(screen)
        screen.fill((255, 255, 255))

        # generate the maze - parameter: corridor length (optional)
        start_time = pygame.time.get_ticks()
        print(f'Generating a maze of {maze.wall_size[1]} x {maze.wall_size[0]} = {maze.wall_size[0] * maze.wall_size[1]} cells. Block dimension = {block_dim}.')
        maze.gen_maze_2D()
        maze.draw_maze()
        print('Ready. Time: {:0.4f} seconds.'.format((pygame.time.get_ticks() - start_time) / 1000.0))
        print('ESC or close the Maze window to end program.')
        print(maze.blocks[:,:])
        
        pygame.event.clear()
        pausing = running    
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

