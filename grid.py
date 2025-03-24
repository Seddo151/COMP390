from settings import Settings
import pygame
import numpy as np

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,128,0)
WHITE = (255,255,255)
BROWN = (165,42,42)
DIM_GREY = (105,105,105)

def diffuse_array(arr, diffusion_rate):
    # Pad the array with zeros so that border cells get treated correctly
    padded = np.pad(arr, ((1,1), (1,1)), mode='constant', constant_values=0)
    # Sum the values of the 8 neighbors using slicing
    neighbors_sum = (
          padded[:-2, 1:-1]  +  # Up
          padded[2:, 1:-1]   +  # Down
          padded[1:-1, :-2]  +  # Left
          padded[1:-1, 2:]   +  # Right
          padded[:-2, :-2]   +  # Top-left
          padded[:-2, 2:]    +  # Top-right
          padded[2:, :-2]    +  # Bottom-left
          padded[2:, 2:]        # Bottom-right
    )
    # Compute the average of neighbors
    neighbors_avg = neighbors_sum / 8.0
    # Return a blend of the original value and neighbors' average
    return (1 - diffusion_rate) * arr + diffusion_rate * neighbors_avg

class Grid:
     
    def __init__(self):
        
        self.rows = Settings.GRID_ROWS
        self.columns = Settings.GRID_COLUMNS
        
        self.food = np.zeros((self.rows, self.columns), dtype=int)
        self.nest = np.zeros((self.rows, self.columns), dtype=bool)
        self.obstacle = np.zeros((self.rows, self.columns), dtype=bool)
        
        self.pheromone_food = np.zeros((self.rows, self.columns), dtype=float)
        self.pheromone_home = np.zeros((self.rows, self.columns), dtype=float)


    def update_pheromones(self):
        decay_rate_food = Settings.DECAY_RATE_FOOD
        decay_rate_home = Settings.DECAY_RATE_HOME
    
        # Multiply all cells by (1 - decay_rate) at once
        self.pheromone_food *= (1 - decay_rate_food)
        self.pheromone_home *= (1 - decay_rate_home)
        
        # Optionally, set very low values to 0 to avoid floating-point artifacts:
        self.pheromone_food[self.pheromone_food < 0.5] = 0
        self.pheromone_home[self.pheromone_home < 0.5] = 0

    def deposit_food_pheromone(self, x, y, amount):
        # Use np.clip to ensure the value doesn't exceed 255
        self.pheromone_food[y, x] = np.clip(self.pheromone_food[y, x] + amount, 0, 255)
    
    def deposit_home_pheromone(self, x, y, amount):
        self.pheromone_home[y, x] = np.clip(self.pheromone_home[y, x] + amount, 0, 255)


    def clear_grid(self):
        self.food.fill(0)
        self.obstacle.fill(False)
        self.nest.fill(False)

    def clear_pheromones(self):
        self.pheromone_food.fill(0)
        self.pheromone_home.fill(0)
                

    def get_cell(self, x, y):
        # Return a dictionary for compatibility if needed.
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return {
                "food": self.food[y, x],
                "nest": self.nest[y, x],
                "obstacle": self.obstacle[y, x],
                "pheromone_food": self.pheromone_food[y, x],
                "pheromone_home": self.pheromone_home[y, x]
            }
        return None
    
    def set_food(self, x, y, amount):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.food[y, x] = max(0, self.food[y, x] + amount)
        
    def set_obstacle(self, x, y, is_obstacle=True):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.obstacle[y, x] = is_obstacle
    
    def set_nest(self, x, y, is_nest=True):
         if 0 <= x < self.columns and 0 <= y < self.rows:
            self.nest[y, x] = is_nest


    def set_pheromone(self, x, y, type, amount = 0):
         if 0 <= x < self.columns and 0 <= y < self.rows:
            if type == 'food':
                # Ensure the value does not exceed a maximum (e.g., 255)
                self.pheromone_food[y, x] = np.clip(self.pheromone_food[y, x] + amount, 0, 255)
            elif type == 'home':
                self.pheromone_home[y, x] = np.clip(self.pheromone_home[y, x] + amount, 0, 255)
            elif type == 'clear':
                self.pheromone_food[y, x] = 0
                self.pheromone_home[y, x] = 0

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
        end_x = min(self.columns - 1, start_x + size - 1)
        end_y = min(self.rows - 1, start_y + size - 1)

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


    def draw_grid(self, screen):
        cell_size = Settings.CELL_SIZE
        grid_colors = np.full((self.rows, self.columns, 3), WHITE, dtype=np.uint8)
        
        # Base layers
        grid_colors[self.obstacle] = DIM_GREY
        grid_colors[self.nest & ~self.obstacle] = BROWN
        grid_colors[(self.food > 0) & ~self.obstacle & ~self.nest] = GREEN
        
        # Pheromone handling
        base_mask = ~(self.obstacle | self.nest | (self.food > 0))
        pheromones = [
            (self.pheromone_food, (255, 'intensity', 255)),  # Pink gradient
            (self.pheromone_home, ('intensity', 255, 255))   # Cyan gradient
        ]
        
        for pheromone, color_template in pheromones:
            mask = (pheromone > 0) & base_mask
            if not np.any(mask):
                continue
            intensity = np.clip(255 - pheromone[mask], 0, 255).astype(np.uint8)
            channels = []
            for c in color_template:
                channels.append(intensity if c == 'intensity' else np.full_like(intensity, c))
            grid_colors[mask] = np.stack(channels, axis=-1)
            base_mask &= ~mask  # Prevent overlap
        
        surface = pygame.surfarray.make_surface(np.transpose(grid_colors, (1, 0, 2)))
        scaled_surface = pygame.transform.scale(
            surface, (self.columns * cell_size, self.rows * cell_size)
        )
        screen.blit(scaled_surface, (0, 0))

    def draw_ants(self, screen, ants, colour):
        cell_size = Settings.CELL_SIZE
        for ant in ants:
            pygame.draw.circle(screen, colour,
                            (ant.x * cell_size + cell_size // 2, ant.y * cell_size + cell_size // 2),
                            cell_size // 3)
            
    def diffuse_pheromones(self):
        diffusion_rate = Settings.PHEROMONE_DIFFUSION_RATE  # e.g., 0.1 or 0.2
        self.pheromone_food = diffuse_array(self.pheromone_food, diffusion_rate)
        self.pheromone_home = diffuse_array(self.pheromone_home, diffusion_rate)

    