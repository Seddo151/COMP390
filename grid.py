import settings

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE 

grid = [[{"pheromone": 0, "food": 0, "nest": 0} for i in range(SCREEN_WIDTH // GRID_SIZE)]
        for i in range(SCREEN_HEIGHT // GRID_SIZE)]

def initialize_food():
        grid[0][0]["food"] = 1

def initialize_nest():
        grid[10][10]["nest"] = 1




