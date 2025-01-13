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
NEST_X = settings.NEST_X
NEST_Y = settings.NEST_Y

#pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ant Colony Simulation")
clock = pygame.time.Clock()
running = True

initialize_food()
initialize_nest()

# Initialize a list of ants
ants = [Ant(NEST_X,
            NEST_Y)
        for _ in range(ANT_NUMBER)]


font = pygame.font.Font(None, 24)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Calculate the grid position
            grid_x = mouse_x // GRID_SIZE
            grid_y = mouse_y // GRID_SIZE
            # Place food on the grid square
            grid[grid_y][grid_x]["food"] += 1
            grid[grid_y][grid_x]["pheromone_food"] = 255
        
    screen.fill("White")
    # RENDER YOUR GAME HERE
    food_collected_count = 0

    for ant in ants:
        ant.move()
        ant.deposit_pheromone(grid)
        ant.change_state(grid)
        food_collected_count += ant.food_collected_count

    update_pheromones()

    draw_grid(screen)
    draw_ants(screen, ants)
    
    text = font.render(f"food collected: {food_collected_count}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(settings.ANT_SPEED)  # limits FPS to 60

pygame.quit()