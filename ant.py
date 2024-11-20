import random
import settings

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "foraging"  # Possible states: "foraging" or "returning"

    def move(self):
        # Basic random movement
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        cols = settings.SCREEN_WIDTH // settings.GRID_SIZE
        rows = settings.SCREEN_HEIGHT // settings.GRID_SIZE
        self.x = max(0, min(self.x + dx, cols - 1))
        self.y = max(0, min(self.y + dy, rows - 1))

    
