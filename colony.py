from ant import Ant
from settings import Settings
from grid import grid

class Colony:
    def __init__(self):
        self.nest_location =  (Settings.NEST_POS_X, Settings.NEST_POS_Y)
        self.species = ""
        self.num_ants = 1000
        self.ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(self.num_ants)]
        self.food_collected = 0

    def reset_ants(self):
        self.ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(self.num_ants)]

    def update_ants(self):
        for ant in self.ants:
            ant.move()
            ant.deposit_pheromone(grid)
            ant.change_state(grid)
            self.food_collected += ant.food_collected_count

        