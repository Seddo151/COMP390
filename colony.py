from ant import Ant
from settings import Settings
from grid import grid

class Colony:
    def __init__(self):
        self.nest_location =  None
        self.species = ""
        self.num_ants = 1000
        self.ants = []
        self.food_collected = 0


    def reset_ants(self):
        if self.nest_location:
            self.ants = [Ant(*self.nest_location, self.nest_location) for _ in range(self.num_ants)]
        else:
            self.ants = []


    def update_ants(self):
        self.food_collected = 0
        for ant in self.ants:
            ant.move()
            ant.deposit_pheromone(grid)
            ant.change_state(grid)
            self.food_collected += ant.food_collected_count

    def place_nest(self, x, y):
        if self.nest_location:
            # Remove the old nest
            old_x, old_y = self.nest_location
            grid[old_y][old_x]["nest"] = False
            grid[old_y][old_x]["pheromone"].clear_pheromone()

        # Place the new nest
        self.nest_location = (x, y)
        grid[y][x]["nest"] = True
        grid[y][x]["pheromone"].deposit_home_pheromone(255)

        # Reset ants to the new nest location
        self.reset_ants()