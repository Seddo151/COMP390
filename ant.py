import random
import settings
from grid import grid


class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "foraging"  # Possible states: "foraging" or "returning"
        self.visited_positions = []  # Memory of recently visited positions

    def move(self):
        current_position = (self.x, self.y)
         # If foraging, follow pheromones or explore randomly
        if self.state == "foraging":
            self.follow_pheromones()
        elif self.state == "returning":
            # When returning, follow pheromones back to the nest
            self.follow_pheromones(inverse=True)

        self.x = max(0, min(self.x, settings.SCREEN_WIDTH // settings.GRID_SIZE - 1))
        self.y = max(0, min(self.y, settings.SCREEN_HEIGHT // settings.GRID_SIZE - 1))

        self.previous_position = current_position

    def follow_pheromones(self, inverse=False):
    
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
        pheromone_threshold = 40 if self.state == "foraging" else 0 # Theshold for faint trails

        cols = (settings.SCREEN_WIDTH // settings.GRID_SIZE) - 1
        rows = (settings.SCREEN_HEIGHT // settings.GRID_SIZE) -1

        

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) in self.visited_positions:
                    continue  # Skip the previous position
                pheromone_level = grid[ny][nx]["pheromone"]
                if pheromone_level > best_pheromone and pheromone_level  > pheromone_threshold: # ignores low lvl pheromoens
                    best_pheromone = pheromone_level
                    best_direction = (dx, dy)

        # Move toward the best pheromone trail, or random if no pheromone detected
        if best_direction and best_pheromone > 0 and random.random() > 0.01:
            dx, dy = best_direction
            
        else:
            # Random exploration if no pheromones are nearby
            dx, dy = random.choice(directions)
            

         # Update visited positions
        self.visited_positions.append((self.x, self.y))
        if len(self.visited_positions) > 50:  # Limit memory to 10 positions
            self.visited_positions.pop(0)

        self.x += dx
        self.y += dy

    def deposit_pheromone(self,grid):
        if self.state == "returning" and grid[self.y][self.x]["pheromone"] < 155 :
            grid[self.y][self.x]["pheromone"] += 15
        elif grid[self.y][self.x]["pheromone"] < 235 and grid[self.y][self.x]["pheromone"] < 10:
            grid[self.y][self.x]["pheromone"] += 0.5

    def change_state(self,grid):
        
        if grid[self.y][self.x]["food"] > 0 and self.state == "foraging" :
            self.state = "returning"
            self.visited_positions = [] # Reset visited positions so it can go back on itself
        elif grid[self.y][self.x]["nest"] > 0 and self.state == "returning" :
            self.state = "foraging"
            self.visited_positions = [] # Reset visited positions so it can go back on itself
    
    

    
