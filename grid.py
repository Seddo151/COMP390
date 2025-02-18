from settings import Settings
from pheromone import Pheromone

grid = [[{"pheromone": Pheromone(Settings.PHEROMONE_DECAY_RATE),
          "food": 0,
          "nest": False,
          "obstacle": False
        }
        for i in range(Settings.SIM_WIDTH // Settings.CELL_SIZE)]
        for i in range(Settings.SIM_HEIGHT // Settings.CELL_SIZE)]

def update_pheromones():
        for row in grid:
            for cell in row:
                if cell["nest"] == False or cell["food"] <= 0:
                    cell["pheromone"].decay()
                    



