from settings import Settings
import pygame
import numpy as np

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
        cell_size = Settings.CELL_SIZE

        # Precomputes all cell rectangles
        self.cell_rects = [
            [
                pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                for j in range(self.columns)
            ]
            for i in range(self.rows)
        ]

        self.food = np.zeros((self.rows, self.columns), dtype=np.uint8)
        self.nest = np.zeros((self.rows, self.columns), dtype=bool)
        self.obstacle = np.zeros((self.rows, self.columns), dtype=bool)
        
        self.pheromone_food = np.zeros((4, self.rows, self.columns), dtype=np.float32)
        self.pheromone_home = np.zeros((4, self.rows, self.columns), dtype=np.float32)

    def decay_pheromones(self):
            self.pheromone_food *= (1 - Settings.DECAY_RATE_FOOD)
            self.pheromone_home *= (1 - Settings.DECAY_RATE_HOME)

            self.pheromone_food[self.pheromone_food < 0.1] = 0
            self.pheromone_home[self.pheromone_home < 0.1] = 0

    def deposit_food_pheromone(self, x, y, amount, colony_id):        
        self.pheromone_food[colony_id, y, x] = min(self.pheromone_food[colony_id, y, x] + amount, 255)

    def deposit_home_pheromone(self, x, y, amount, colony_id):
        self.pheromone_home[colony_id, y, x] = min(self.pheromone_home[colony_id, y, x] + amount, 255)

    def clear_grid(self):
        self.food.fill(0)
        self.obstacle.fill(False)
        self.nest.fill(False)

    def clear_pheromones(self):
        self.pheromone_food.fill(0.0)
        self.pheromone_home.fill(0.0)

    def set_food(self, x, y, amount):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.food[y, x] = max(0, self.food[y, x] + amount)
        
    def set_obstacle(self, x, y, is_obstacle=True):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.obstacle[y, x] = is_obstacle
    
    def set_nest(self, x, y, is_nest=True):
         if 0 <= x < self.columns and 0 <= y < self.rows:
            self.nest[y, x] = is_nest

    def update_food_pheromone(self, x, y, amount, colony_id):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            new_value = self.pheromone_food[colony_id, y, x] + amount
            new_value = max(0, min(new_value, 255))
            self.pheromone_food[colony_id, y, x] = new_value

    def update_home_pheromone(self, x, y, amount, colony_id):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            new_value = self.pheromone_home[colony_id, y, x] + amount
            new_value = max(0, min(new_value, 255))
            self.pheromone_home[colony_id, y, x] = new_value

   

    def modify_item(self, pos, action, size, type):
        cell_size = Settings.CELL_SIZE
        food_num = Settings.FOOD_NUM
        # Gets the mouse position
        mouse_x, mouse_y = pos
        # Calculatse the grid position
        grid_x = mouse_x // cell_size
        grid_y = mouse_y // cell_size

        # Calculates the start and end positions for the item placement
        start_x = max(0, grid_x - size // 2)
        start_y = max(0, grid_y - size // 2)
        end_x = min(self.columns - 1, start_x + size - 1)
        end_y = min(self.rows - 1, start_y + size - 1)

        # Places items in the calculated area
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if action == 'place':
                    if type == 'food':
                        self.set_food(x, y, food_num)
                    elif type == 'obstacle':
                        self.set_obstacle(x, y)
                    
                elif action == 'delete':
                    if  type == 'food':
                        # Removes food on the grid square
                        self.set_food(x, y, -food_num)
                    if  type == 'obstacle':
                        self.set_obstacle(x, y, False)

    def draw_grid(self, screen):
        cell_size = Settings.CELL_SIZE
        grid_colors = np.full((self.rows, self.columns, 3), WHITE, dtype=np.uint8)
        
        # sets colours (obstacle is displayed infront of nest and nest infront of food)
        grid_colors[self.obstacle] = DIM_GREY
        grid_colors[self.nest & ~self.obstacle] = BROWN  
        grid_colors[(self.food > 0) & ~self.obstacle & ~self.nest] = GREEN
        
        # base mask for the pheromones
        base_mask = ~(self.obstacle | self.nest | (self.food > 0))
        
        # Food pheromone overlay 
        food_max = np.max(self.pheromone_food, axis=0)

        show_food = (food_max > 0) & base_mask
        if np.any(show_food):
            strength = food_max[show_food]
            intensity = np.clip(255 - strength, 0, 255).astype(np.uint8)
            r = np.full(intensity.shape, 255, dtype=np.uint8)
            g = intensity
            b = np.full(intensity.shape, 255, dtype=np.uint8)
            grid_colors[show_food] = np.stack((r, g, b), axis=-1)
            base_mask &= ~show_food 
        # Home pheromone overlay
        home_max = np.max(self.pheromone_home, axis=0)
        show_home = (home_max > 0) & base_mask

        if np.any(show_home):
            strength = home_max[show_home]
            intensity = np.clip(255 - strength, 0, 255).astype(np.uint8)
            r = intensity
            g = np.full(intensity.shape, 255, dtype=np.uint8)
            b = np.full(intensity.shape, 255, dtype=np.uint8)
            grid_colors[show_home] = np.stack((r, g, b), axis=-1)
        
        # Renders grid to screen
        screen.blit(
            pygame.transform.scale(
                pygame.surfarray.make_surface(np.transpose(grid_colors, (1, 0, 2))),
                (self.columns * cell_size, self.rows * cell_size)),
                (0, 0)
        )
    

    def draw_ants(self, screen, ants, colour):
        cell_size = Settings.CELL_SIZE
        for ant in ants:
            pygame.draw.circle(screen, colour,
                            (ant.x * cell_size + cell_size // 2, ant.y * cell_size + cell_size // 2),
                            cell_size // 3)
            
    

    