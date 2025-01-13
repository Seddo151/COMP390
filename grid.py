import settings

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE
NEST_X = settings.NEST_X
NEST_Y = settings.NEST_Y      

grid = [[{"pheromone_food": 0,"pheromone_home": 0, "food": 0, "nest": 0} for i in range(SCREEN_WIDTH // GRID_SIZE)]
        for i in range(SCREEN_HEIGHT // GRID_SIZE)]

def initialize_food():
        grid[24][32]["food"] = 1
        grid[24][32]["pheromone_food"] = 255

def initialize_nest():
        grid[NEST_X][NEST_Y]["nest"] = 1
        grid[NEST_X][NEST_Y]["pheromone_home"] = 255
       




