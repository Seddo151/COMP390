from ant import Ant
from settings import Settings

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

        if self.nest_location:
            # Remove the old nest
            old_x, old_y = self.nest_location
            grid.set_nest(old_x, old_y, False)
            grid.set_pheromone(old_x, old_y, 'clear')


        # Place the new nest
        self.nest_location = (grid_x, grid_y)
        grid.set_nest(grid_x, grid_y, True)
        grid.set_pheromone(grid_x, grid_y, 'home', 255)
        # Reset ants to the new nest location
        self.reset_ants()