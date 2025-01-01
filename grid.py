import settings

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE
nest_x = 10
nest_y = 10 

grid = [[{"pheromone": 0, "food": 0, "nest": 0} for i in range(SCREEN_WIDTH // GRID_SIZE)]
        for i in range(SCREEN_HEIGHT // GRID_SIZE)]

def initialize_food():
        grid[20][20]["food"] = 1

def initialize_nest():
        grid[nest_x][nest_x]["nest"] = 1
        grid[nest_x][nest_x]["pheromone"] = 255




