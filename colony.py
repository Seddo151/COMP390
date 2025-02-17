from ant import Ant
from settings import Settings

class Colony:
    def __init__(self):
        self.nest_location =  (0,0)
        self.species = ""
        self.num_ants = 0
        self.ants = [Ant(self.nest_location) for _ in range(self.num_ants)]
        self.food_collected = 0

    def reset_ants(self):
        self.ants = [Ant(self.nest_location) for _ in range(self.num_ants)]   