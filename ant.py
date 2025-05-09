import random
from settings import Settings

class Ant:
    def __init__(self, x, y, nest_location, species, colony_id):
        self.colony_id = colony_id
        self.nest_location = nest_location
        self.x = x
        self.y = y
        self.has_food = False  # Possible states: "foraging" or "returning"
        self.last_direction = (0, 0) # Last Direction
        self.returning_timer = 0  # Timer for the returning state
        self.food_collected_count = 0

        self.memory_size = Settings.ANT_MEMORY_SIZE
        self.visited_positions = []  # List of recently visited positions

        self.colour = species[0]
        self.rand_nums = species[1] # change chances of actions in follow_pheromone func
        self.allignment_weight = species[2] # changes how much an ant knows about direction of nest
        self.food_size_pheromone = species[3] # changes amount of pheromones deposited based on food sources size
        self.food_found = 0
        

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

        if self.returning_timer > 800: 
            self.has_food = False
            self.returning_timer = 0  # Resets the timer


        self.follow_pheromones(grid)
        self.x = max(0, min(self.x, grid.columns - 1))
        self.y = max(0, min(self.y, grid.rows - 1))

        # Updates visited positions
        current_position = (self.x, self.y)
        self.visited_positions.append(current_position)
        if len(self.visited_positions) > self.memory_size:  # Limits the memorys
                self.visited_positions.pop(0)

    def follow_pheromones(self, grid):
        best_score, best_direction, possible_directions, best_score2, best_direction2 = self.find_best(grid)

        rand = random.random
        r1, r2, r3 = rand(), rand(), rand()
        # Introduce randomness to break loops
        if possible_directions == []:
            dx, dy = (0,0)
        elif best_direction and best_score  > 0 and r1 > self.rand_nums[0]: # chance to move randomly
            if best_direction2 and best_score2  > 0 and r2 > self.rand_nums[1]: #chance to take 2nd best direction
                dx, dy = best_direction2
            else:
                dx, dy = best_direction
        else:
            if self.last_direction in possible_directions and r3 > self.rand_nums[2]:  # chance to continue
                dx, dy = self.last_direction
            else:
                dx, dy = random.choice(possible_directions)  # Explore randomly

        self.last_direction = (dx, dy)
        self.x += dx
        self.y += dy

    def find_best(self, grid):
        directions = self.directions
        current_x, current_y = self.x, self.y
        has_food = self.has_food
        colony_id = self.colony_id

        columns, rows = grid.columns, grid.rows
        obstacle = grid.obstacle
        pheromone_home = grid.pheromone_home
        pheromone_food = grid.pheromone_food
        grid_food = grid.food
        grid_nest = grid.nest
        

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
            if obstacle[ny, nx]:
                continue

            possible_directions.append((dx, dy))

            visited_penalty = 400 if (nx, ny) in self.visited_positions else 0
            
            pheromone_level = pheromone_home[colony_id][ny, nx] if has_food else pheromone_food[colony_id][ny, nx]
            # Combine pheromone level with nest alignment for returning ants only
            direction_alignment = (dx * nest_dx + dy * nest_dy) if has_food else 0
            score = pheromone_level + (self.allignment_weight * direction_alignment) - visited_penalty

            cell_food = grid_food[ny, nx]
            cell_nest = grid_nest[ny, nx]


            if cell_food > 0 and not has_food:
                self.food_found = cell_food
                score = 1000
            elif cell_nest and has_food:
                score = 1000

            if score > best_score:
                best_score2 = best_score
                best_score = score
                best_direction2 = best_direction
                best_direction = (dx, dy)
        
        return best_score , best_direction, possible_directions, best_score2, best_direction2

   
    def deposit_pheromone(self,grid):
        if self.last_direction != (0,0):
            if self.has_food == True:
                if self.food_size_pheromone:
                    if self.food_found > 150: 
                        grid.deposit_food_pheromone(self.x, self.y, 40, self.colony_id)
                    else:
                        grid.deposit_food_pheromone(self.x, self.y, 4, self.colony_id)
                else:
                    grid.deposit_food_pheromone(self.x, self.y, 6, self.colony_id)
            else:
                grid.deposit_home_pheromone(self.x, self.y, 6, self.colony_id)

    
    def change_state(self,grid):
        
        food = grid.food[self.y, self.x]
        nest = grid.nest[self.y, self.x]

        if food > 0 and self.has_food == False:
            self.has_food = True
            self.visited_positions = [] # Reset visited positions
            grid.set_food(self.x, self.y, -1)

        
        elif nest == True and self.has_food == True:
            self.has_food = False
            self.visited_positions = [] # Reset visited positions
            self.food_collected_count += 1
            self.last_direction=(0,0)
            
    
    def calculate_nest_direction(self):
        nest_x, nest_y = self.nest_location
        dx = nest_x - self.x
        dy = nest_y - self.y
        magnitude = max(1, (dx**2 + dy**2)**0.5)  
        return dx / magnitude, dy / magnitude  # Unit vector toward the nest

   

