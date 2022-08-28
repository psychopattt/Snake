from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w

# Colors
MENU_BG = (40, 40, 40)
BG_COLOR = (31, 31, 31)
BG_COLOR_LIGHT = (36, 36, 36)
TEXT_COLOR = (200, 200, 200)
WALL_COLOR = (80, 80, 80)
SNACK_COLOR = (120, 0, 150)
HEAD_COLORS = [
    (40, 111, 17), 
    (230, 25, 75), 
    (255, 225, 25), 
    (0, 130, 200), 
    (245, 130, 48), 
    (70, 240, 240), 
    (240, 50, 230), 
    (210, 245, 60), 
    (250, 190, 212), 
    (0, 128, 128), 
    (170, 110, 40), 
    (128, 0, 0), 
    (255, 250, 200), 
    (128, 128, 0), 
    (255, 215, 180), 
    (0, 0, 128)
]

# Snake inputs
SNAKE_DIRECTION_INPUTS = [K_DOWN, K_LEFT, K_RIGHT, K_UP, K_w, K_d, K_s, K_a]
DIRECTION_TOP = [K_UP, K_w]
DIRECTION_RIGHT = [K_RIGHT, K_d]
DIRECTION_DOWN = [K_DOWN, K_s]
DIRECTION_LEFT = [K_LEFT, K_a]

# Default game settings
DEFAULT_GAME_WIDTH = 24
DEFAULT_GAME_HEIGHT = 18
DEFAULT_BLOCK_SIZE = 30
DEFAULT_GAME_FRAMETIME = 125
DEFAULT_NB_SNACKS = 1
DEFAULT_NB_PLAYERS = 1
GAME_INPUT_FPS = 200

# Menu settings
SIZE_X = 550
SIZE_Y = 630
MENU_FPS = 60
MENU_INPUT_FRAMETIME = 1000 / MENU_FPS / 1000 # Seconds