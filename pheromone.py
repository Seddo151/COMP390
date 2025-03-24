class Pheromone:
    def __init__(self, decay_rate):
        self.pheromone_food = 0
        self.pheromone_home = 0
        self.decay_rate = decay_rate

    def deposit_food_pheromone(self, amount):
        self.pheromone_food = min(255, self.pheromone_food + amount)
        
    def deposit_home_pheromone(self, amount):
        self.pheromone_home = min(255, self.pheromone_home + amount)

    def clear_pheromone(self):
        self.pheromone_home = 0
        self.pheromone_food = 0

    def decay(self):
        if self.pheromone_food < 0.5:
            self.pheromone_food = 0
        else:
            self.pheromone_food = max(0, self.pheromone_food * (1 - self.decay_rate))

        if self.pheromone_home < 0.5:
            self.pheromone_home = 0
        else:
            self.pheromone_home = max(0, self.pheromone_home * (1 - self.decay_rate))
        

    