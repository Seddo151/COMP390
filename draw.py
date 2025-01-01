import pygame
import settings
from grid import grid

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE 


def draw_grid(screen):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if cell["food"] > 0  :
                 color = "green"
            elif cell["nest"] > 0  :
                 color = "brown" 
            elif cell["pheromone"] > 0:
                 color = (255,255 - cell["pheromone"],255)
            else:
                 color = (255, 255, 255)
            pygame.draw.rect(screen, color, rect, 100) # use 100 to fill grid squares
            
def draw_ants(screen, ants):
        for ant in ants:
            pygame.draw.circle(screen, (0, 0, 0), (ant.x * GRID_SIZE + GRID_SIZE // 2, ant.y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)

def update_pheromones():
    for row in grid:
        for cell in row:
            if cell.get("nest",0):
               cell["pheromone"] = max(0, cell["pheromone"] - settings.DECAY_RATE)

