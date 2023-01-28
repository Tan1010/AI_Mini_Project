from sys import exit

import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT)

from Agent.agent import agent
from ant import Ant
from game_constants import (DARK_BROWN, DARKER_BROWN, DISPLAY_DIM, DURATION,
                            FPS, GAME_TITLE, GAME_TITLE_POS, LEVEL_POS, LIGHT_RED,
                            RECT_DIM, RECT_POS, RECT_THICKNESS, RED, SCORE_POS,
                            SUGAR_CENTER_1, SUGAR_CENTER_2, SUGAR_COUNT,
                            TIMER_POS, TITLE, TITLE_POS, WHITE, Direction)
from MazeGenerator.maze import Maze


class Game:
    def __init__(self, maze_type='rb', agent_type='bfs', fps=FPS, duration=DURATION, evaluate_maze=False):
        # Initialize the game
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = None
        self.running = True
        self.maze_type = maze_type
        self.evaluate_maze = evaluate_maze
        self.fps = fps

        # Maze and game states
        self.maze = Maze(method=self.maze_type, evaluate=self.evaluate_maze)
        self.level = 1
        self.score = 0
        self.sugar_hold = 0
        self.next_level = True 

        # Agent
        self.agent = agent(agent_type)
        self.directions = []  # for AI agents
        
        # Timer
        self.duration = duration
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

    def initialize_display(self):
        # Screen
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

        # Music
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("Assets/main_bgm.mp3")
        pygame.mixer.music.play(loops=-1)
        self.take_sugar_bgm = pygame.mixer.Sound("Assets/take_sugar_bgm.mp3")
        self.take_sugar_bgm.set_volume(0.1)
        self.put_sugar_at_home_bgm = pygame.mixer.Sound("Assets/put_sugar_at_home_bgm.mp3")
        self.put_sugar_at_home_bgm.set_volume(0.1)
        self.next_game_bgm = pygame.mixer.Sound("Assets/next_game_bgm.mp3")
        self.next_game_bgm.set_volume(0.1)
        self.game_over_bgm = pygame.mixer.Sound("Assets/game_over_bgm.mp3")
        self.game_over_bgm.set_volume(0.2)

        pygame.display.update()

    def update_game(self, direction):
        self.next_level = False     
        move = False
        ant_neighbour = self.maze.get_ant_neighbour(direction)
        # 0: path, 1: wall, 2: home, 3: sugar, 4: ant, 5: visited
        if ant_neighbour == 0:
            move = True
        if ant_neighbour == 2:
            self.score += self.sugar_hold
            self.sugar_hold = 0
            self.put_sugar_at_home_bgm.play() if self.screen else None
        if ant_neighbour == 3 and self.sugar_hold < 2:
            self.sugar_hold += 1
            self.take_sugar_bgm.play() if self.screen else None
            move = True
        if move:
            self.maze.update(direction)
            self.ant.update_position(direction) if self.screen else None

        # Advance to next level
        if self.score == self.level*SUGAR_COUNT:
            self.next_level = True
            self.level += 1
            self.maze = Maze(method=self.maze_type, evaluate=self.evaluate_maze)

        if self.screen:
            if self.next_level:
                self.maze.initialize_display(self.screen)
                self.next_game_bgm.play()
                self.ant = Ant(self.screen, self.maze)
            else:
                self.ant.update_orientation(direction)
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
        timer_text = self.text_font.render(str(self.duration), True, DARKER_BROWN)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(
            RECT_POS[1][0]+5, RECT_POS[1][1]+5, RECT_DIM[0]-10, RECT_DIM[1]-10))
        self.screen.blit(timer_text, TIMER_POS)
        pygame.display.update()

    def run(self):
        self.initialize_display()
        gg_flag = False
        while(self.running):
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                elif event.type == self.timer_event:
                    if self.duration > 0:
                        self.duration -= 1
                    if self.screen:
                        self.update_timer_display()

            # waiting user to quit game when time is out
            if self.duration == 0:
                if not gg_flag:
                    self.game_over_bgm.play(loops=-1)
                    gg_font = pygame.font.Font(None, 100)
                    gg_text = gg_font.render("GAMEOVER", True, RED)
                    pygame.draw.rect(self.screen, LIGHT_RED, pygame.Rect(
                        55, 370, 450, 100))
                    self.screen.blit(gg_text, (80, 390))
                    pygame.display.update()
                    gg_flag = True
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

            self.clock.tick(self.fps)

        pygame.quit()
        exit()


if __name__ == '__main__':
    print("Welcome to Ant Game!")
    maze_index = int(input("Select maze type {0: Recursive Backtracking; 1: Kruskal's Algorithm}: "))
    agent_index = int(input("Select agent type {0: Backtracking; 1: BFS; 2: Human}: "))
    fps = int(input("Enter FPS: "))
    duration = int(input("Enter duration: "))
    evaluate = int(input("Run maze evaluation (number of junctions) {0: False; 1: True}: "))

    maze_type = ['rb', 'krus']
    agent_type = ['backtracking', 'bfs', 'human']
    game = Game(maze_type=maze_type[maze_index], agent_type=agent_type[agent_index], fps=fps, duration=duration, evaluate_maze=evaluate)
    game.run()
