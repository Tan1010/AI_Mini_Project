from enum import Enum

# Display
DISPLAY_DIM = (700, 700)

# Maze
BLOCK_DIM = 20
MAZE_SIZE = (12, 12)
MAZE_POS = (30, 170)

# Sugar
SUGAR_COUNT = 20

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (92, 64, 51) 
DARKER_BROWN = (48, 19, 1)

# Rectangle
RECT_THICKNESS = 2
RECT_DIM = (110, 75)
RECT_POS = [(560, 75), (560, 205), (560, 335), (560, 465), (560, 595)]

# Game title
GAME_TITLE = "THE ANT GAME"
GAME_TITLE_POS = (90, 80)

# Title 
TITLE = ["LEVEL", "TIME", "SCORE", "SUGAR 1", "SUGAR 2"]
TITLE_POS = [(560, 50), (560, 180), (560, 310), (560, 440), (560, 570)]

# Rectangle content
LEVEL_POS = (595, 95)
TIMER_POS = (595, 225)
SCORE_POS = (595, 355)
SUGAR_CENTER_1 = (615, 500)
SUGAR_CENTER_2 = (615, 630)

# Directions
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)