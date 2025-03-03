from settings import Settings
from pheromone import Pheromone
import pygame

class Grid:
     
    def __init__(self):

        self.grid = [[{"pheromone": Pheromone(Settings.PHEROMONE_DECAY_RATE),
                    "food": 0,
                    "nest": False,
                    "obstacle": False}
                    for i in range(Settings.SIM_WIDTH // Settings.CELL_SIZE)]
                    for i in range(Settings.SIM_HEIGHT // Settings.CELL_SIZE)]

    def update_pheromones(self):
        for row in self.grid:
            for cell in row:
                if cell["nest"] == False or cell["food"] <= 0:
                    cell["pheromone"].decay()
                
    def reset_grid(self):
        for row in self.grid:
            for cell in row:
                cell["food"] = 0
                cell["obstacle"] = False
                # cell["nest"] = False

    def reset_pheromones(self):
        for row in self.grid:
            for cell in row:
                cell["pheromone"].pheromone_food = 0
                cell["pheromone"].pheromone_home = 0

    def get_cell(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x]
        return None
    
    def set_food(self, x, y, amount):
        cell = self.get_cell(x,y)
        if cell:
            cell["food"] = amount
        
    def set_obstacle(self, x, y, is_obstacle=True):
        cell = self.get_cell(x,y)
        if cell:
            cell["obstacle"] = is_obstacle
    
    def set_nest(self, x, y, is_nest=True):
        cell = self.get_cell(x,y)
        if cell:
            cell["obstacle"] = is_nest












    def draw_grid(self, screen):
        cell_size = Settings.CELL_SIZE
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell = self.grid[row][col]
                pheromone = cell["pheromone"]

                if cell["obstacle"]:
                    colour = "dimgrey"
                elif cell["nest"]:
                    colour = "brown" 
                elif cell["food"] > 0:
                    colour = "green"
                elif pheromone.pheromone_food > 0:
                    colour = (255,255 - pheromone.pheromone_food,255)
                elif pheromone.pheromone_home > 0:
                    colour = (255 - pheromone.pheromone_home,255,255)
                else:
                    colour = (255, 255, 255)

                screen.fill(colour, rect=[col * cell_size, row * cell_size, cell_size, cell_size])

    def draw_ants(self, screen, ants):
        cell_size = Settings.CELL_SIZE
        for ant in ants:
            pygame.draw.circle(screen, (0, 0, 0),
                                (ant.x * cell_size + cell_size // 2, ant.y * cell_size + cell_size // 2),
                                cell_size // 3)