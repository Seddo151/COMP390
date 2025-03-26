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

        # Precompute all cell rectangles
        self.cell_rects = [
            [
                pygame.Rect(
                    j * cell_size,
                    i * cell_size,
                    cell_size,
                    cell_size
                )
                for j in range(self.columns)
            ]
            for i in range(self.rows)
        ]

        self.food = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.nest = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        self.obstacle = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        
        self.pheromone_food = [[0.0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.pheromone_home = [[0.0 for _ in range(self.columns)] for _ in range(self.rows)]


    def update_pheromones(self):
        self.pheromone_food = np.array(self.pheromone_food) * (1 - Settings.DECAY_RATE_FOOD)
        self.pheromone_home = np.array(self.pheromone_home) * (1 - Settings.DECAY_RATE_HOME)
        # Thresholding (optional)
        self.pheromone_food[self.pheromone_food < 0.5] = 0
        self.pheromone_home[self.pheromone_home < 0.5] = 0

    def deposit_food_pheromone(self, x, y, amount):        
        self.pheromone_food[y][x] = min(int(self.pheromone_food[y][x]) + amount, 255)
    
    def deposit_home_pheromone(self, x, y, amount):
        self.pheromone_home[y][x] = min(int(self.pheromone_home[y][x]) + amount, 255)


    def clear_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.food[i][j] = 0
                self.obstacle[i][j] = False
                self.nest[i][j] = False

    def clear_pheromones(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.pheromone_food[i][j] = 0.0
                self.pheromone_home[i][j] = 0.0

    def set_food(self, x, y, amount):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.food[y][x] = max(0, self.food[y][x] + amount)
        
    def set_obstacle(self, x, y, is_obstacle=True):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.obstacle[y][x] = is_obstacle
    
    def set_nest(self, x, y, is_nest=True):
         if 0 <= x < self.columns and 0 <= y < self.rows:
            self.nest[y][x] = is_nest

    def update_food_pheromone(self, x, y, amount):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            new_value = self.pheromone_food[y][x] + amount
            # Clip the value between 0 and 255
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            self.pheromone_food[y][x] = new_value

    def update_home_pheromone(self, x, y, amount):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            new_value = self.pheromone_home[y][x] + amount
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            self.pheromone_home[y][x] = new_value

    def clear_pheromone_cell(self, x, y):
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.pheromone_food[y][x] = 0.0
            self.pheromone_home[y][x] = 0.0

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


    def get_cell_colour(self, i, j):
        if self.obstacle[i][j]:
            return DIM_GREY
        if self.nest[i][j]:
            return BROWN
        if self.food[i][j]:
            return GREEN
        if self.pheromone_food[i][j] > 0:
            blue = int(255 - self.pheromone_food[i][j])
            return (255, blue, 255)
        if self.pheromone_home[i][j] > 0:
            red = int(255 - self.pheromone_home[i][j])
            return (red, 255, 255)
        return WHITE

    


    def draw_grid(self, screen):
        cell_size = Settings.CELL_SIZE
        grid_colors = np.full((self.rows, self.columns, 3), WHITE, dtype=np.uint8)
        
        food = np.array(self.food)
        nest = np.array(self.nest)
        obstacle = np.array(self.obstacle)
        pheromone_food = np.array(self.pheromone_food)
        pheromone_home = np.array(self.pheromone_home)


        # Base layers
        grid_colors[obstacle] = DIM_GREY
        grid_colors[nest & ~obstacle] = BROWN
        grid_colors[(food > 0) & ~obstacle & ~nest] = GREEN
        
        # Pheromone handling
        base_mask = ~(obstacle | nest | (food > 0))
        pheromones = [
            (pheromone_food, (255, 'intensity', 255)),  # Pink gradient
            (pheromone_home, ('intensity', 255, 255))   # Cyan gradient
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
            
    

    