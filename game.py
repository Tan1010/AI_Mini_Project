from sys import exit

import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT)

from Agent.agent import agent
from ant import Ant
from game_constants import (DARK_BROWN, DARKER_BROWN, DISPLAY_DIM, FPS,
                            GAME_TITLE, GAME_TITLE_POS, LEVEL_POS, RECT_DIM,
                            RECT_POS, RECT_THICKNESS, SCORE_POS,
                            SUGAR_CENTER_1, SUGAR_CENTER_2, SUGAR_COUNT,
                            TIMER_DURATION, TIMER_POS, TITLE, TITLE_POS, WHITE,
                            Direction)
from MazeGenerator.maze import Maze


class Game:
    def __init__(self, display=True, maze_type='rb', agent_type='human'):
        # Initialize the game
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.screen = None
        self.running = True
        self.display = display
        self.maze_type = maze_type

        # Maze and game states
        self.maze = Maze(method=self.maze_type, evaluate=True)
        self.level = 1
        self.score = 0
        self.sugar_hold = 0
        self.next_level = True 

        # Agent
        self.agent = agent(agent_type)
        self.directions = []  # for AI agents
        
        # Timer
        self.timer_duration = TIMER_DURATION
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
    
    def initialize_display(self):
        # add bgm here
        if self.display:
            self.screen = pygame.display.set_mode(DISPLAY_DIM)
            self.screen.fill(WHITE)
            pygame.display.set_caption('Ant Game')

            # Maze and Ant
            self.maze.initialize_display(self.screen)
            self.ant = Ant(self.screen, self.maze)
            
            # All titles
            game_title_font = pygame.font.Font(None, 70)
            game_title_surface = game_title_font.render(GAME_TITLE, True, DARKER_BROWN)
            self.screen.blit(game_title_surface, GAME_TITLE_POS)
            title_font = pygame.font.Font(None, 35)
            title_surfaces = [title_font.render(title, True, DARKER_BROWN) for title in TITLE]
            [self.screen.blit(title_surfaces[i], TITLE_POS[i]) for i in range(len(title_surfaces))]

            # All bounding boxes
            [pygame.draw.rect(self.screen, DARK_BROWN, (*pos, *RECT_DIM), RECT_THICKNESS) for pos in RECT_POS]

            # Game state
            self.text_font = pygame.font.Font(None, 50)
            self.sugar_surface = pygame.image.load("Assets/sugar.png")
            self.sugar_surface = pygame.transform.scale(self.sugar_surface, (55,55))
            self.update_display()

            pygame.display.update()

    def turn_off_display(self):
        self.display = False
        self.screen = None
        self.maze.screen = None

    def update_game(self, direction):
        self.next_level = False     # TODO prompt AI to turn_off_display
        move = False
        ant_neighbour = self.maze.get_ant_neighbour(direction)
        # 0: path, 1: wall, 2: home, 3: sugar, 4: ant
        if ant_neighbour == 0:
            # encounter path
            move = True
        if ant_neighbour == 2:
            # sent sugar home, can add bool variable for music
            self.score += self.sugar_hold
            self.sugar_hold = 0
        if ant_neighbour == 3 and self.sugar_hold < 2:
            # get sugar, can add bool variable for music
            self.sugar_hold += 1
            move = True
        if move:
            self.maze.update(direction)
            self.ant.update_position(direction) if self.screen else None

        # Advance to next level
        if self.score == self.level*SUGAR_COUNT:
            self.next_level = True
            self.level += 1
            self.maze = Maze(method=self.maze_type, evaluate=True)

        if self.screen:
            if self.next_level:
                # add music here (advance to next level)
                self.maze.initialize_display(self.screen)
                self.ant = Ant(self.screen, self.maze)
            else:
                self.ant.update_orientation(direction)
            # add conditional code here to add music here (get/return sugar)
            self.update_display()

    def update_display(self):
        # Level
        level_text = self.text_font.render(str(self.level), True, DARKER_BROWN)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            RECT_POS[0][0]+5, RECT_POS[0][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
        self.screen.blit(level_text, LEVEL_POS)
        # Score
        score_text = self.text_font.render(str(self.score), True, DARKER_BROWN)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            RECT_POS[2][0]+5, RECT_POS[2][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
        self.screen.blit(score_text, SCORE_POS)
        # Sugar hold
        sugar_rect = self.sugar_surface.get_rect()
        if self.sugar_hold == 0:
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(
                RECT_POS[3][0]+5, RECT_POS[3][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(
                RECT_POS[4][0]+5, RECT_POS[4][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
        else:
            sugar_rect.center = SUGAR_CENTER_1 if self.sugar_hold == 1 else SUGAR_CENTER_2
            self.screen.blit(self.sugar_surface, sugar_rect)
        # Ant
        self.ant.update_display()

        pygame.display.update()

    def update_timer_display(self):
        timer_text = self.text_font.render(str(self.timer_duration), True, DARKER_BROWN)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            RECT_POS[1][0]+5, RECT_POS[1][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
        self.screen.blit(timer_text, TIMER_POS)
        pygame.display.update()
    
    def run(self):
        self.initialize_display()
        
        while(self.running):
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == self.timer_event:
                    if self.timer_duration > 0:
                        self.timer_duration -= 1
                    if self.screen:
                        self.update_timer_display()

            # waiting user to quit game when time is out
            if self.timer_duration == 0:
                # add end game text here
                # end game music here
                continue
                        
            if self.agent:
                if not self.directions:
                    self.directions += self.agent.solve(self)
                self.update_game(self.directions.pop(0))
            
            else:
                pressed_keys = pygame.key.get_pressed()
                if (pressed_keys[K_UP]):
                    self.update_game(Direction.UP)
                elif (pressed_keys[K_LEFT]):
                    self.update_game(Direction.LEFT)
                elif (pressed_keys[K_DOWN]):
                    self.update_game(Direction.DOWN)
                elif (pressed_keys[K_RIGHT]):
                    self.update_game(Direction.RIGHT)

            self.clock.tick(FPS)

        pygame.quit()
        exit()


if __name__ == '__main__':
    game = Game(maze_type='krus', agent_type='bfs')
    game.run()
