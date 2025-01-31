from settings import Settings
from pheromone import Pheromone

grid = [[{"pheromone": Pheromone(Settings.PHEROMONE_DECAY_RATE), "food": 0, "nest": 0}
        for i in range(Settings.SCREEN_WIDTH // Settings.CELL_SIZE)]
        for i in range(Settings.SCREEN_HEIGHT // Settings.CELL_SIZE)]

def initialize_nest():
        grid[Settings.NEST_POS_X][Settings.NEST_POS_Y]["nest"] = 1
        grid[Settings.NEST_POS_X][Settings.NEST_POS_Y]["pheromone"].deposit_home_pheromone(255)
          
def update_pheromones():
        for row in grid:
            for cell in row:
                if cell["nest"] <= 0 or cell["food"] <= 0:
                    cell["pheromone"].decay()
                    



