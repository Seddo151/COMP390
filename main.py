import pygame
import settings
import random
from draw import draw_grid, draw_ants, update_pheromones
from ant import Ant
from grid import grid, initialize_food, initialize_nest

SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
GRID_SIZE = settings.GRID_SIZE
ANT_NUMBER = settings.ANT_NUMBER

#pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Colony Simulation")
clock = pygame.time.Clock()
running = True

initialize_food()
initialize_nest()

# Initialize a list of ants
ants = [Ant(random.randint(0, settings.SCREEN_WIDTH // settings.GRID_SIZE - 1),
            random.randint(0, settings.SCREEN_HEIGHT // settings.GRID_SIZE - 1))
        for _ in range(ANT_NUMBER)]




while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("White")
    # RENDER YOUR GAME HERE

    for ant in ants:
        ant.move()
        ant.deposit_pheromone(grid)
        ant.change_state(grid)

    update_pheromones()

    draw_grid(screen)
    draw_ants(screen, ants)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()