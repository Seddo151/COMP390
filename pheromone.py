class Pheromone:
    def __init__(self, decay_rate):
        self.pheromone_food = 0
        self.pheromone_home = 0
        self.decay_rate = decay_rate
        self.last_reinforced = 1

    def deposit_food_pheromone(self, amount):
        self.pheromone_food = min(255, self.pheromone_food + amount)
        self.last_reinforced = 1

    def deposit_home_pheromone(self, amount):
        self.pheromone_home = min(255, self.pheromone_home + amount)

    def decay(self):
        self.pheromone_food = max(0, self.pheromone_food - (self.decay_rate * self.last_reinforced))
        self.pheromone_home = max(0, self.pheromone_home - self.decay_rate)
        #self.last_reinforced += 1

    def set_last_reinforced(self):
        self.last_reinforced = 1