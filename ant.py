import random
from settings import Settings
from grid import grid

class Ant:
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.has_food = False  # Possible states: "foraging" or "returning"
        self.visited_positions = []  # List of recently visited positions
        self.last_direction = (0, 0) # Last Direction
        self.returning_timer = 0  # Timer for returning state
        self.food_collected_count = 0
       

    def move(self):

        # Increment timer if in the returning state
        if self.has_food == True:
            self.returning_timer += 1
        else:
            self.returning_timer = 0

        if self.returning_timer > 200:  # Timeout returning limit 
            self.has_food = False
            self.returning_timer = 0  # Reset the timer


        self.follow_pheromones()
        self.x = max(0, min(self.x, Settings.GRID_COLUMNS))
        self.y = max(0, min(self.y, Settings.GRID_ROWS))

        # Update visited positions
        current_position = (self.x, self.y)
        self.visited_positions.append(current_position)
        if len(self.visited_positions) > Settings.ANT_MEMORY_SIZE:  # Limit memory to 20 positions
            self.visited_positions.pop(0)


    def follow_pheromones(self):
    
        directions = [
        (0, 1), # Up
          (1, 0), # Right
            (0, -1), # Down
              (-1, 0), # Left
        (1, 1), # Up-right
          (1, -1), # Up-left
            (-1, 1), # Down-right
              (-1, -1) # Down-left
        ]
         
       
        best_score, best_direction, possible_directions = self.find_best(directions)
        # Introduce randomness to break loops
        if possible_directions == []:
            dx, dy = (0,0)
        elif best_direction and best_score  > 0 and random.random() > 0.05: # % chance to move randomly
            dx, dy = best_direction
        else:
            if self.last_direction in possible_directions and random.random() > 0.1:  # % chance to continue
                dx, dy = self.last_direction
            else:
                dx, dy = random.choice(possible_directions)  # Explore randomly


        self.last_direction = (dx, dy)
        self.x += dx
        self.y += dy


    def find_best(self, directions):
        best_direction = None
        best_score = -float('inf')
        possible_directions = []
        # Calculate the direction of the nest
        nest_dx, nest_dy = self.calculate_nest_direction()  

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy

            # Skip out-of-bounds directions
            if not (0 <= nx <= Settings.GRID_COLUMNS and 0 <= ny <= Settings.GRID_ROWS):
                continue

            # skips directions blocked by obstacles
            if grid[ny][nx]["obstacle"]:
                continue

            possible_directions.append((dx, dy))

            if (nx, ny) in self.visited_positions:
                continue  # Skip the previous position
            
            pheromone_level = (
            grid[ny][nx]["pheromone"].pheromone_food if self.has_food == False
            else grid[ny][nx]["pheromone"].pheromone_home
            )
            # Combine pheromone level with nest alignment for returning ants only
            direction_alignment = (dx * nest_dx + dy * nest_dy) if self.has_food else 0
            score = pheromone_level + 0.5 * direction_alignment

            if score > best_score:
                best_score = score
                best_direction = (dx, dy)
        
        return best_score , best_direction, possible_directions

   
    def deposit_pheromone(self,grid):
        
        if self.has_food == True:
            grid[self.y][self.x]["pheromone"].deposit_food_pheromone(1)
            #grid[self.y][self.x]["pheromone"].set_last_reinforced()
        else:
            grid[self.y][self.x]["pheromone"].deposit_home_pheromone(1)

    
    def change_state(self,grid):
        
        if grid[self.y][self.x]["food"] > 0 and self.has_food == False:
            self.has_food = True
            self.visited_positions = [] # Reset visited positions
            grid[self.y][self.x]["food"] -= 1 

        elif grid[self.y][self.x]["nest"] == True and self.has_food == True:
            self.has_food = False
            self.visited_positions = [] # Reset visited positions
            self.food_collected_count += 1
            
    
    def calculate_nest_direction(self):
        dx = Settings.NEST_POS_X - self.x
        dy = Settings.NEST_POS_Y - self.y
        magnitude = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        return dx / magnitude, dy / magnitude  # Unit vector toward the nest

   
