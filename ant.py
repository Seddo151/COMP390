import random
import settings

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "foraging"  # Possible states: "foraging" or "returning"

    def move(self):
        # Basic random movement
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        cols = settings.SCREEN_WIDTH // settings.GRID_SIZE
        rows = settings.SCREEN_HEIGHT // settings.GRID_SIZE
        self.x = max(0, min(self.x + dx, cols - 1))
        self.y = max(0, min(self.y + dy, rows - 1))

    def deposit_pheromone(self,grid):
        if self.state == "returning" and grid[self.y][self.x]["pheromone"] < 155 :
            grid[self.y][self.x]["pheromone"] += 100
        elif grid[self.y][self.x]["pheromone"] < 235:
            grid[self.y][self.x]["pheromone"] += 20

    def change_state(self,grid):
        if grid[self.y][self.x]["food"] > 0 :
            self.state = "returning"
        elif grid[self.y][self.x]["nest"] > 0 :
            self.state = "foraging"
    
