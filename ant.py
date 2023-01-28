import numpy as np
import pygame
from pygame.locals import RLEACCEL

from game_constants import BLACK, BLOCK_DIM, MAZE_POS, WHITE, Direction


class Ant(pygame.sprite.Sprite):
    def __init__(self, screen, maze):
        # Initialize
        self.screen = screen
        pos = np.where(maze.blocks==4)
        initial_y, initial_x = pos[0].item(), pos[1].item()

        # Ant image
        self.surface = pygame.image.load("Assets/ant.png").convert()
        self.surface.set_colorkey(BLACK, RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (BLOCK_DIM, BLOCK_DIM))
        
        # Spawn the ant at its starting position
        self.rect = self.surface.get_rect()
        self.rect.move_ip(MAZE_POS[0] + initial_x*BLOCK_DIM, MAZE_POS[1] + initial_y*BLOCK_DIM)
        self.orientation  = "RIGHT"

    # Move ant's sprite
    def update_position(self, direction):
        dy, dx = direction.value
        self.rect.move_ip(dx*BLOCK_DIM, dy*BLOCK_DIM)        

    def update_orientation(self, direction):
        if direction == Direction.LEFT:
            self.orientation = "LEFT"
        elif direction == Direction.RIGHT:
            self.orientation = "RIGHT"

    def update_display(self):
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
                self.rect.left, self.rect.top, BLOCK_DIM, BLOCK_DIM))
        if self.orientation == "RIGHT":
            self.screen.blit(pygame.transform.flip(self.surface, True, False), self.rect)
        else: 
            self.screen.blit(self.surface, self.rect)