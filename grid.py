from settings import Settings
from pheromone import Pheromone
import pygame

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,128,0)
WHITE = (255,255,255)
BROWN = (165,42,42)
DIM_GREY = (105,105,105)



class Grid:
     
    def __init__(self):
        
        self.rows = Settings.GRID_ROWS
        self.columns = Settings.GRID_COLUMNS

        self._grid = [[{"pheromone": Pheromone(Settings.PHEROMONE_DECAY_RATE),
                    "food": 0,
                    "nest": False,
                    "obstacle": False}
                    for i in range(Settings.SIM_WIDTH // Settings.CELL_SIZE)]
                    for i in range(Settings.SIM_HEIGHT // Settings.CELL_SIZE)]

    def update_pheromones(self):
        for row in self._grid:
            for cell in row:
                if cell["nest"] == False or cell["food"] <= 0:
                    cell["pheromone"].decay()
                
    def reset_grid(self):
        for row in self._grid:
            for cell in row:
                cell["food"] = 0
                cell["obstacle"] = False
                cell["nest"] = False

    def reset_pheromones(self):
        for row in self._grid:
            for cell in row:
                cell["pheromone"].clear_pheromone()
                

    def get_cell(self, x, y):
        if 0 <= x < len(self._grid[0]) and 0 <= y < len(self._grid):
            return self._grid[y][x]
        return None
    
    def set_food(self, x, y, amount):
        cell = self.get_cell(x,y)
        if cell:
            cell["food"] = max(0, cell["food"] + amount)
        
    def set_obstacle(self, x, y, is_obstacle=True):
        cell = self.get_cell(x,y)
        if cell:
            cell["obstacle"] = is_obstacle
    
    def set_nest(self, x, y, is_nest=True):
        cell = self.get_cell(x,y)
        if cell:
            cell["nest"] = is_nest


    def set_pheromone(self, x, y, type, amount = 0):
        cell = self.get_cell(x,y)
        if cell:
            if type == 'food':
                cell["pheromone"].deposit_food_pheromone(amount)
            elif type == 'home':
                cell["pheromone"].deposit_home_pheromone(amount)
            elif type == 'clear':
                cell["pheromone"].clear_pheromone()


    def modify_item(self, pos, action, size, type):
        cell_size = Settings.CELL_SIZE
        food_num = Settings.FOOD_NUM
        # Get the mouse position
        mouse_x, mouse_y = pos
        # Calculate the grid position
        grid_x = mouse_x // cell_size
        grid_y = mouse_y // cell_size

        # Calculate the start and end positions for the item placement
        start_x = max(0, grid_x - size // 2)
        start_y = max(0, grid_y - size // 2)
        end_x = min(len(self._grid[0]) - 1, start_x + size - 1)
        end_y = min(len(self._grid) - 1, start_y + size - 1)

        # Place items in the calculated area
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if action == 'place':
                    if type == 'food':
                        self.set_food(x, y, food_num)
                    elif type == 'obstacle':
                        self.set_obstacle(x, y)
                    
                elif action == 'delete':
                    if  type == 'food':
                        # Remove food on the grid square
                        self.set_food(x, y, -food_num)
                    if  type == 'obstacle':
                        self.set_obstacle(x, y, False)
                    if type == 'nest':
                        self.set_nest(x, y, False)


    def draw_grid(self, screen):
        cell_size = Settings.CELL_SIZE
        for row in range(len(self._grid)):
            for col in range(len(self._grid[0])):
                cell = self._grid[row][col]
                pheromone = cell["pheromone"]

                if cell["obstacle"]:
                    colour = DIM_GREY
                elif cell["nest"]:
                    colour = BROWN
                elif cell["food"] > 0:
                    colour = GREEN
                elif pheromone.pheromone_food > 0:
                    colour = (255,round(255 - pheromone.pheromone_food),255)
                elif pheromone.pheromone_home > 0:
                    colour = (round(255 - pheromone.pheromone_home),255,255)
                else:
                    colour = WHITE

                screen.fill(colour, rect=[col * cell_size, row * cell_size, cell_size, cell_size])

    def draw_ants(self, screen, ants, colour):
        cell_size = Settings.CELL_SIZE
        for ant in ants:
            pygame.draw.circle(screen, colour,
                                (ant.x * cell_size + cell_size // 2, ant.y * cell_size + cell_size // 2),
                                cell_size // 3)
            