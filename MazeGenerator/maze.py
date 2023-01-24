from sys import exit

import numpy as np
import pygame
from PIL import Image
from scipy import signal

from game_constants import (BLOCK_DIM, DARK_BROWN, MAZE_POS, MAZE_SIZE,
                            SUGAR_COUNT, WHITE)

from .Kruskal import Kruskal
from .RecursiveBacktracking import RecursiveBacktracking


class Maze:
    def __init__(self, method='rb', evaluate=False):
        self.screen = None 
        self.block_size = tuple(size*2+1 for size in MAZE_SIZE)
        self.maze_generator = RecursiveBacktracking(*MAZE_SIZE) if method.strip().lower() == 'rb' else Kruskal(*MAZE_SIZE)

        # Generate walls
        self.blocks = self.maze_generator.generate()
        # Evaluate maze
        if evaluate:
            print(f'Maze: score = {self.evaluate()}')
        # Generate home and ant spawn point
        self.blocks[1, 0] = 2   # home
        self.blocks[1, 1] = 4  # ant spawn point
        # Generate sugars
        flatten = self.blocks.reshape(-1)
        flatten[np.random.choice(np.where(flatten == 0)[0], SUGAR_COUNT)] = 3  # replace SUGAR_COUNT = 20 path cells with sugars

    def initialize_display(self, screen):
        self.screen = screen 
        wall_color = np.array(DARK_BROWN, dtype=np.uint8)
        sugar_img_arr = np.array(Image.open('Assets\sugar_small.jpg').convert('RGB'))
        home_img_arr = np.array(Image.open('Assets\home.jpg').convert('RGB'))
        # Wall
        surface_arr = np.zeros((*self.block_size, 3), dtype=np.int16) + 255
        surface_arr[self.blocks==1] = wall_color
        surface_arr = surface_arr.repeat(BLOCK_DIM, axis=0).repeat(BLOCK_DIM, axis=1)
        # Home
        surface_arr[BLOCK_DIM:2*BLOCK_DIM, :BLOCK_DIM] = home_img_arr
        # Sugar
        arr_x_sugar, arr_y_sugar = np.where(self.blocks==3)
        arr_x_sugar, arr_y_sugar = arr_x_sugar*BLOCK_DIM, arr_y_sugar*BLOCK_DIM        
        for x, y in zip(arr_x_sugar, arr_y_sugar):
            surface_arr[x:x+BLOCK_DIM, y:y+BLOCK_DIM] = sugar_img_arr
        # Whole maze
        surface = pygame.surfarray.make_surface(np.transpose(surface_arr, [1,0,2]))
        self.screen.blit(surface, MAZE_POS)

    def evaluate(self):
        junction_filter = np.array([[0,1,0],[1,2,1],[0,1,0]])
        junction_map = signal.convolve2d(self.blocks, junction_filter, mode='same', boundary='fill', fillvalue=1)
        self.score = (junction_map < 2).sum()
        return self.score

    def get_ant_neighbour(self, direction):
        ant_pos = np.where(self.blocks==4)
        ant_y = ant_pos[0].item()
        ant_x = ant_pos[1].item()
        ant_dy, ant_dx = direction.value
        return self.blocks[ant_y+ant_dy][ant_x+ant_dx]

    def update(self, direction):
        ant_pos = np.where(self.blocks==4)
        ant_y = ant_pos[0].item()
        ant_x = ant_pos[1].item()
        ant_dy, ant_dx = direction.value
        if self.screen:
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(
                MAZE_POS[0]+ant_x*BLOCK_DIM, MAZE_POS[1]+ant_y*BLOCK_DIM, BLOCK_DIM, BLOCK_DIM))
            if self.blocks[ant_y+ant_dy][ant_x+ant_dx] == 3:
                pygame.draw.rect(self.screen, WHITE, pygame.Rect(
                    MAZE_POS[0]+(ant_x+ant_dx)*BLOCK_DIM, MAZE_POS[1]+(ant_y+ant_dy)*BLOCK_DIM, BLOCK_DIM, BLOCK_DIM))
        self.blocks[ant_y+ant_dy][ant_x+ant_dx] = 4
        self.blocks[ant_y][ant_x] = 0

# # To be removed
# if __name__ == '__main__':

#     # Run and display the Maze.
#     # Left mouse button or space bar: generate a new maze. 
#     # ESC or close the window: Quit.

#     # Set screen size and initialize it
#     pygame.display.init()

#     # Setup the clock for a decent framerate TODO
#     clock = pygame.time.Clock()

#     block_dim = 20  # block size in pixels
#     disp_size = (700, 700)
#     screen = pygame.display.set_mode(disp_size)
#     pygame.display.set_caption('Ant Game')
#     running = True

#     while running:
#         maze = Maze(screen)  # Change Maze Generator Algo here 
#         screen.fill((255, 255, 255))

#         start_time = pygame.time.get_ticks()
#         print(f'Generating a maze of {maze.block_size[1]} x {maze.block_size[0]} = {maze.block_size[0] * maze.block_size[1]} cells.')
#         maze.initialize()
#         maze.update_display()
#         print('Ready. Time: {:0.4f} seconds.'.format((pygame.time.get_ticks() - start_time) / 1000.0))
#         print('ESC or close the Maze window to end program.')
#         print(maze.blocks[:,:])
        
#         pygame.event.clear()
#         pausing = running    
#         while pausing:
#             event = pygame.event.wait()  # wait for user input, yielding to other prcesses
#             if event.type == pygame.QUIT:
#                 pausing = False
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     pausing = False
#                 if event.key == pygame.K_ESCAPE:
#                     pausing = False
#                     running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     # left button: new maze
#                     pausing = False

#     # exit; close display
#     pygame.quit()
#     exit()

