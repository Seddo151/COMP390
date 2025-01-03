import random
import settings
from grid import grid


class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "foraging"  # Possible states: "foraging" or "returning"
        self.visited_positions = []  # Memory of recently visited positions
        self.path_stack = []  # Stack to remember the path
        self.last_direction = (0, 0)

    def move(self):
        current_position = (self.x, self.y)
        
        if self.state == "foraging":
            self.follow_pheromones()
        elif self.state == "returning":
            self.retrace_path()

        
        self.x = max(0, min(self.x, settings.SCREEN_WIDTH // settings.GRID_SIZE - 1))
        self.y = max(0, min(self.y, settings.SCREEN_HEIGHT // settings.GRID_SIZE - 1))

         # Update visited positions
        self.visited_positions.append(current_position)
        if len(self.visited_positions) > 10:  # Limit memory to 10 positions
            self.visited_positions.pop(0)

    def follow_pheromones(self):
    
        directions = [
        (0, 1),   # Down
        (1, 0),   # Right
        (0, -1),  # Up
        (-1, 0),  # Left
        (1, 1),   # Bottom-right
        (1, -1),  # Top-right
        (-1, 1),  # Bottom-left
        (-1, -1)  # Top-left
    ]
        best_direction = None
        best_pheromone = -1 
        

        cols = (settings.SCREEN_WIDTH // settings.GRID_SIZE) - 1
        rows = (settings.SCREEN_HEIGHT // settings.GRID_SIZE) -1

        

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) in self.visited_positions:
                    continue  # Skip the previous position
                pheromone_level = grid[ny][nx]["pheromone_food"] 
                if pheromone_level > best_pheromone :
                    best_pheromone = pheromone_level
                    best_direction = (dx, dy)

       

        # Momentum Bias: Favor last direction if no strong pheromones are present
        if best_direction is None or best_pheromone <= 5:  # Low pheromone threshold
            if self.last_direction in directions and random.random() > 0.05:  # 80% chance to continue
                dx, dy = self.last_direction
            else:
                dx, dy = random.choice(directions)  # Explore randomly
        else:
            dx, dy = best_direction
   
        self.path_stack.append((self.x, self.y)) 
        self.last_direction = (dx, dy)
        self.x += dx
        self.y += dy

    def retrace_path(self):
        if self.path_stack:
            # Pop the last position from the stack and move there
            self.x, self.y = self.path_stack.pop()
        else:
            # Fallback to random movement
            directions = [
                (0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]
            dx, dy = random.choice(directions)
            self.x += dx
            self.y += dy

    def deposit_pheromone(self,grid):
        
        if self.state == "returning" and grid[self.y][self.x]["pheromone_food"] < 200 :
            grid[self.y][self.x]["pheromone_food"] += 15
        elif self.state == "foraging" and  grid[self.y][self.x]["pheromone_home"] < 200 :
            if grid[self.y][self.x]["pheromone_food"] > 5:
                grid[self.y][self.x]["pheromone_home"] += 10
            elif grid[self.y][self.x]["pheromone_food"] < 5 :
                grid[self.y][self.x]["pheromone_home"] += 5

    
    def change_state(self,grid):
        
        if grid[self.y][self.x]["food"] > 0 and self.state == "foraging" :
            self.state = "returning"
            self.visited_positions = [] # Reset visited positions so it can go back on itself
        elif grid[self.y][self.x]["nest"] > 0 and self.state == "returning" :
            self.state = "foraging"
            self.visited_positions = [] # Reset visited positions so it can go back on itself
            self.path_stack = []

   

    
