import pygame
from settings import Settings
from draw import draw_grid, draw_ants
from ant import Ant
from grid import grid, initialize_nest, update_pheromones

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Calculate the grid position
            grid_x = mouse_x // Settings.CELL_SIZE
            grid_y = mouse_y // Settings.CELL_SIZE
            # Place food on the grid square
            grid[grid_y][grid_x]["food"] += Settings.FOOD_NUM
            grid[grid_y][grid_x]["pheromone"].deposit_food_pheromone(255)

    return True
        
def update_ants(ants):
    food_collected_count = 0

    for ant in ants:
        ant.move()
        ant.deposit_pheromone(grid)
        ant.change_state(grid)
        food_collected_count += ant.food_collected_count

    return food_collected_count


def main():

    #pygame setup
    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Ant Colony Simulation")
    clock = pygame.time.Clock()
    running = True

    initialize_nest()

    # Initialize a list of ants
    ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(Settings.TOTAL_ANTS)]

    font = pygame.font.Font(None, 24)
 
    while running:
        running = event_handler()

        screen.fill("White")
        
        food_collected_count = update_ants(ants)
        update_pheromones() 

        draw_grid(screen)
        draw_ants(screen, ants)
        
        text = font.render(f"food collected: {food_collected_count}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # flip() the display to put your work on screen
        pygame.display.flip() 
        clock.tick(Settings.FPS)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()