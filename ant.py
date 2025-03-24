import random
from settings import Settings

class Ant:
    def __init__(self, x, y, nest_location, species):
        self.nest_location = nest_location
        self.x = x
        self.y = y
        self.has_food = False  # Possible states: "foraging" or "returning"
        self.visited_positions = []  # List of recently visited positions
        self.last_direction = (0, 0) # Last Direction
        self.returning_timer = 0  # Timer for returning state
        self.food_collected_count = 0

        
        self.memory_size = Settings.ANT_MEMORY_SIZE
        self.colour = species[0]
        self.rand_nums = species[1] # change chances of actions in follow_pheromone func
        self.directional_allignment = species[2] # changes how much an ant knows about direction of nest

        self.directions = ( # all possible directions
            (0,0), # None
            (0, 1), # Up
            (1, 0), # Right
            (0, -1), # Down
            (-1, 0), # Left
            (1, 1), # Up-right
            (1, -1), # Up-left
            (-1, 1), # Down-right
            (-1, -1) # Down-left
        ) 
       

    def move(self, grid):

        # Increment timer if in the returning state
        if self.has_food == True:
            self.returning_timer += 1
        else:
            self.returning_timer = 0

        if self.returning_timer > 600:  # Timeout returning limit 
            self.has_food = False
            self.returning_timer = 0  # Reset the timer


        self.follow_pheromones(grid)
        self.x = max(0, min(self.x, grid.columns - 1))
        self.y = max(0, min(self.y, grid.rows - 1))

        # Update visited positions
        current_position = (self.x, self.y)
        self.visited_positions.append(current_position)
        if len(self.visited_positions) > self.memory_size:  # Limit memory to 20 positions
            self.visited_positions.pop(0)


    def follow_pheromones(self, grid):
       
        best_score, best_direction, possible_directions, best_score2, best_direction2 = self.find_best(grid)

        rand = random.random
        # Introduce randomness to break loops
        if possible_directions == []:
            dx, dy = (0,0)
        elif best_direction and best_score  > 0 and rand() > self.rand_nums[0]: # chance to move randomly
            if best_direction2 and best_score2  > 0 and rand() > self.rand_nums[1]: #chance to take 2nd best direction
                dx, dy = best_direction2
            else:
                dx, dy = best_direction
        else:
            if self.last_direction in possible_directions and rand() > self.rand_nums[2]:  # chance to continue
                dx, dy = self.last_direction
            else:
                dx, dy = random.choice(possible_directions)  # Explore randomly


        self.last_direction = (dx, dy)
        self.x += dx
        self.y += dy


    def find_best(self, grid):
        
        directions = self.directions
        current_x, current_y = self.x, self.y
        visited = self.visited_positions
        columns, rows = grid.columns, grid.rows
        has_food = self.has_food

        nest_dx, nest_dy = (0, 0)
        if has_food:
            nest_dx, nest_dy = self.calculate_nest_direction()  # Calculate the direction of the nest

        best_direction = None
        best_direction2 = None
        best_score = -float('inf')
        best_score2 = -float('inf')
        possible_directions = []

        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            
            # Skip out-of-bounds directions
            if not (0 <= nx < columns and 0 <= ny < rows):
                continue

            
            
            # skips directions blocked by obstacles
            if grid.obstacle[ny, nx]:
                continue

            possible_directions.append((dx, dy))

            visited_penalty = 100 if (nx, ny) in visited else 0
            
            pheromone_level = grid.pheromone_home[ny, nx] if has_food else grid.pheromone_food[ny, nx]
            # Combine pheromone level with nest alignment for returning ants only
            direction_alignment = (dx * nest_dx + dy * nest_dy) if has_food else 0
            score = pheromone_level + (5.0 * direction_alignment) - visited_penalty

            cell_food = grid.food[ny, nx]
            cell_nest = grid.nest[ny, nx]


            if cell_food > 0 and not has_food:
                score = 256
            elif cell_nest and has_food:
                score = 256

            if score > best_score:
                best_score2 = best_score
                best_score = score
                best_direction2 = best_direction
                best_direction = (dx, dy)
        
        return best_score , best_direction, possible_directions, best_score2, best_direction2

   
    def deposit_pheromone(self,grid):
        if self.last_direction != (0,0):
            if self.has_food == True:
                grid.set_pheromone(self.x, self.y, 'food', 4)
            else:
                grid.set_pheromone(self.x, self.y, 'home', 4)

    
    def change_state(self,grid):
        cell = grid.get_cell(self.x, self.y)
        if cell is None:
            # Option 1: Clamp the coordinates (or log an error)
            return
        
        if cell["food"] > 0 and self.has_food == False:
            self.has_food = True
            self.visited_positions = [] # Reset visited positions
            grid.set_food(self.x, self.y, -1)

        elif cell["nest"] == True and self.has_food == True:
            self.has_food = False
            self.visited_positions = [] # Reset visited positions
            self.food_collected_count += 1
            self.last_direction=(0,0)
            
    
    def calculate_nest_direction(self):
        nest_x, nest_y = self.nest_location
        dx = nest_x - self.x
        dy = nest_y - self.y
        magnitude = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
        return dx / magnitude, dy / magnitude  # Unit vector toward the nest

   

