import pygame
from settings import Settings
from draw import draw_grid, draw_ants
from ant import Ant
from grid import grid, initialize_nest, update_pheromones
from gui import Button, TextBox


def handle_event(button_play, button_pause, button_reset, button_obstacle, button_food, placing_food, placing_obstacle, mouse_dragging, paused):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_food, placing_obstacle, mouse_dragging, paused
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button pressed
            mouse_dragging = True
            print("Mouse dragging started")
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
            mouse_dragging = False
            print("Mouse dragging ended")
        if event.type == pygame.MOUSEMOTION and mouse_dragging:  # Mouse is being dragged
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Calculate the grid position
            grid_x = mouse_x // Settings.CELL_SIZE
            grid_y = mouse_y // Settings.CELL_SIZE

            if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
                if placing_food:
                    # Place food on the grid square
                    grid[grid_y][grid_x]["food"] += Settings.FOOD_NUM
                    grid[grid_y][grid_x]["pheromone"].deposit_food_pheromone(255)
                elif placing_obstacle:
                    grid[grid_y][grid_x]["obstacle"] = True

        if button_play.is_clicked(event):
            paused = False
            print("Button Clicked!")  # Action when button is clicked
        if button_pause.is_clicked(event):
            paused = True
            print("Pause Button Clicked!")  
        if button_reset.is_clicked(event):
            print("Reset Button Clicked!")
        
        if button_food.is_clicked(event):
            placing_food = True
            placing_obstacle = False
        if button_obstacle.is_clicked(event):
            placing_obstacle = True
            placing_food = False

    return True, placing_food, placing_obstacle, mouse_dragging, paused


    
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


    # Create GUI elements
    button_play = Button("Play", (1320, 40), (100, 50))
    button_pause = Button("Pause", (1490, 40), (100, 50))
    button_reset = Button("Reset", (1650, 40), (100, 50))

    button_food = Button("Food", (1320, 120), (100, 50))
    button_obstacle = Button("Obstacle", (1490, 120), (100, 50))
    button_nest = Button("Nest", (1650, 120), (100, 50))

    text_box = TextBox((1000, 200), (200, 40))

    placing_food = True
    placing_obstacle = False
    mouse_dragging = False
    paused = False


    initialize_nest()

    # Initialize a list of ants
    ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(Settings.TOTAL_ANTS)]

    font = pygame.font.Font(None, 24)
 
    while running:
        running, placing_food, placing_obstacle, mouse_dragging, paused = handle_event(button_play, button_pause, button_reset, button_obstacle, button_food, placing_food, placing_obstacle, mouse_dragging, paused)

        screen.fill("White")
        
        if not paused:
            food_collected_count = update_ants(ants)
            update_pheromones()
        
        
       
        draw_grid(screen)
        draw_ants(screen, ants)

        # Draw elements
        pygame.draw.rect(screen, (200, 200, 200) , pygame.Rect((1280, 0), (500, 920)))
        pygame.draw.rect(screen, (200, 200, 200) , pygame.Rect((0, 720), (1280, 200)))

        button_play.draw(screen)
        button_pause.draw(screen)
        button_reset.draw(screen)

        button_food.draw(screen)
        button_obstacle.draw(screen)
        button_nest.draw(screen)

        text_box.draw(screen)

        text = font.render(f"food collected: {food_collected_count}", True, (0, 0, 0))
        screen.blit(text, (10, 750))

        # flip() the display to put your work on screen
        pygame.display.flip() 
        clock.tick(Settings.FPS)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()