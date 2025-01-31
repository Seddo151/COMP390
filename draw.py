import pygame
from settings import Settings
from grid import grid

def draw_grid(screen):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            rect = pygame.Rect(col * Settings.CELL_SIZE, row * Settings.CELL_SIZE, Settings.CELL_SIZE, Settings.CELL_SIZE)
            if cell["food"] > 0  :
                 color = "green"
            elif cell["nest"] > 0  :
                 color = "brown" 
            elif cell["pheromone"].pheromone_food > 0:
                 color = (255,255 - cell["pheromone"].pheromone_food,255)
            elif cell["pheromone"].pheromone_home > 0:
                 color = (255 - cell["pheromone"].pheromone_home,255,255)
            else:
                 color = (255, 255, 255)
            pygame.draw.rect(screen, color, rect, 100) # use 100 to fill grid squares
            
def draw_ants(screen, ants):
        for ant in ants:
            pygame.draw.circle(screen, (0, 0, 0), (ant.x * Settings.CELL_SIZE + Settings.CELL_SIZE // 2, ant.y * Settings.CELL_SIZE + Settings.CELL_SIZE // 2), Settings.CELL_SIZE // 3)




