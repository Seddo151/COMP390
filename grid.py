import pygame
import settings
import sys

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE 



grid = [[{"pheromone": 0, "food": 0} for i in range(SCREEN_WIDTH // GRID_SIZE)]
        for i in range(SCREEN_HEIGHT // GRID_SIZE)]


def draw_grid(screen):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = (0, 255, 0) if cell["food"] > 0 else (200, 200, 200)
            pygame.draw.rect(screen, color, rect, 1)



