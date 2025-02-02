import pygame
from settings import Settings
from grid import grid

def draw_grid(screen):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            rect = pygame.Rect(col * Settings.CELL_SIZE, row * Settings.CELL_SIZE, Settings.CELL_SIZE, Settings.CELL_SIZE)
            if cell["obstacle"] == True:
                 colour = "dimgrey"
            elif cell["nest"] == True :
                 colour = "brown" 
            elif cell["food"] > 0  :
                 colour = "green"
            elif cell["pheromone"].pheromone_food > 0:
                 colour = (255,255 - cell["pheromone"].pheromone_food,255)
            elif cell["pheromone"].pheromone_home > 0:
                 colour = (255 - cell["pheromone"].pheromone_home,255,255)
            else:
                 colour = (255, 255, 255)
            pygame.draw.rect(screen, colour, rect, 100) # use 100 to fill grid squares
            
def draw_ants(screen, ants):
        for ant in ants:
            pygame.draw.circle(screen, (0, 0, 0), (ant.x * Settings.CELL_SIZE + Settings.CELL_SIZE // 2, ant.y * Settings.CELL_SIZE + Settings.CELL_SIZE // 2), Settings.CELL_SIZE // 3)




