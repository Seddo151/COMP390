import random
import settings
from grid import grid

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE
NEST_X = settings.NEST_X
NEST_Y = settings.NEST_Y

class Ant:
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.state = "foraging"  # Possible states: "foraging" or "returning"
        self.visited_positions = []  # List of recently visited positions
        self.last_direction = (0, 0) # Last Direction
        self.returning_timer = 0  # Timer for returning state
        self.food_collected_count = 0 

    def move(self):

        # Increment timer if in the returning state
        if self.state == "returning":
            self.returning_timer += 1
        else:
            self.returning_timer = 0

        if self.returning_timer > 200:  # Timeout returning limit 
            self.state = "foraging"
            self.returning_timer = 0  # Reset the timer

        self.follow_pheromones()
      
        self.x = max(0, min(self.x, SCREEN_WIDTH // GRID_SIZE - 1))
        self.y = max(0, min(self.y, SCREEN_HEIGHT // GRID_SIZE - 1))

        # Update visited positions
        current_position = (self.x, self.y)
        self.visited_positions.append(current_position)
        if len(self.visited_positions) > 20:  # Limit memory to 20 positions
            self.visited_positions.pop(0)

    def follow_pheromones(self):
    
        directions = [
        (0, 1), (1, 0), (0, -1), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
        best_direction = None
        best_score = -float('inf')
        # Calculate the direction of the nest
        nest_dx, nest_dy = self.calculate_nest_direction()  

        cols = (SCREEN_WIDTH // GRID_SIZE) - 1
        rows = (SCREEN_HEIGHT // GRID_SIZE) -1


        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy

            # Skip out-of-bounds directions
            if not (0 <= nx <= cols and 0 <= ny <= rows):
                continue

            if (nx, ny) in self.visited_positions:
                continue  # Skip the previous position
            
            pheromone_level = (
            grid[ny][nx]["pheromone_food"] if self.state == "foraging"
            else grid[ny][nx]["pheromone_home"]
            )
            # Combine pheromone level with nest alignment for returning ants only
            direction_alignment = (dx * nest_dx + dy * nest_dy) if self.state == "returning" else 0
            score = pheromone_level + 0.5 * direction_alignment

            if score > best_score:
                best_score = score
                best_direction = (dx, dy)

 
        if best_direction and best_score  > 0 and random.random() > 0.005: # % chance to move randomly
            dx, dy = best_direction
        else:
            if self.last_direction in directions and random.random() > 0.05:  # % chance to continue
                dx, dy = self.last_direction
            else:
                dx, dy = random.choice(directions)  # Explore randomly


        self.last_direction = (dx, dy)
        self.x += dx
        self.y += dy

   

    def deposit_pheromone(self,grid):
        
        if self.state == "returning" and grid[self.y][self.x]["pheromone_food"] < 200 :
            grid[self.y][self.x]["pheromone_food"] += 5
        elif self.state == "foraging" and  grid[self.y][self.x]["pheromone_home"] < 200 :
            if grid[self.y][self.x]["pheromone_food"] > 5:
                grid[self.y][self.x]["pheromone_home"] += 5
            elif grid[self.y][self.x]["pheromone_food"] <= 5 and grid[self.y][self.x]["pheromone_home"] < 150 :
                grid[self.y][self.x]["pheromone_home"] += 1

    
    def change_state(self,grid):
        
        if grid[self.y][self.x]["food"] > 0 and self.state == "foraging" :
            self.state = "returning"
            self.visited_positions = [] # Reset visited positions 
        elif grid[self.y][self.x]["nest"] > 0 and self.state == "returning" :
            self.state = "foraging"
            self.visited_positions = [] # Reset visited positions
            self.food_collected_count += 1
            

    def calculate_nest_direction(self):
        dx = NEST_X - self.x
        dy = NEST_Y - self.y
        magnitude = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        return dx / magnitude, dy / magnitude  # Unit vector toward the nest

   
