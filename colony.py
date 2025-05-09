from ant import Ant
from settings import Settings



class Colony:
    def __init__(self, species, colony_id):
        self.colony_id = colony_id
        self.nest_location =  None
        self.species = species
        self.num_ants = Settings.DEFAULT_NUM_ANTS
        self.ants = []
        self.food_collected = 0

    def reset_ants(self, grid):
        if self.nest_location:
            if  0 <= self.nest_location[0] < grid.columns and 0 <= self.nest_location[1] < grid.rows:
                self.ants = [Ant(*self.nest_location, self.nest_location, self.species, self.colony_id) for _ in range(self.num_ants)]
        else:
            self.ants = []

    def update_ants(self, grid):
        self.food_collected = 0
        for ant in self.ants:
            ant.move(grid)
            ant.deposit_pheromone(grid)
            ant.change_state(grid)
            self.food_collected += ant.food_collected_count

    def move_nest(self, grid, pos):
        cell_size = Settings.CELL_SIZE
        x, y = pos
        grid_x = x // cell_size
        grid_y = y // cell_size

        if not (0 <= grid_x < grid.columns and 0 <= grid_y < grid.rows):
            return  # Ignores  if its out-of-bounds

        if self.nest_location:
            # Removes the old nest
            old_x, old_y = self.nest_location
            grid.set_nest(old_x, old_y, False)

        # Places the new nest
        self.nest_location = (grid_x, grid_y)
        grid.set_nest(grid_x, grid_y, True)
        # Resets the ants to the new nest location
        self.reset_ants(grid)