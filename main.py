import pygame
import random
from settings import Settings
from draw import draw_grid, draw_ants
from ant import Ant
from grid import grid, initialize_nest, update_pheromones
from gui import Button, TextBox

class Simulation:
    def __init__(self):

        pygame.init()

        self.settings = Settings()
        self.cursor_size = 1
        self.running = True
        self.paused = False
        self.placing_food = True
        self.placing_obstacle = False
        self.placing_nest = False
        self.mouse1_dragging = False
        self.mouse3_dragging = False
        self.num_ants = Settings.DEFAULT_NUM_ANTS
        self.ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(self.num_ants)]

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Ant Colony Simulation")

        # Create GUI elements
        self.button_pause = Button("Pause", (1320, 40), (100, 50))
        self.button_reset = Button("Reset", (1650, 40), (100, 50))

        self.button_food = Button("Food", (1320, 120), (100, 50))
        self.button_obstacle = Button("Obstacle", (1490, 120), (100, 50))
        self.button_nest = Button("Nest", (1650, 120), (100, 50))

        self.text_box_ants = TextBox((1450, 240), (100, 40), 4, str(self.num_ants))
        self.button_reset_ants = Button("Reset Ants", (1600, 240), (100, 50))
        
        self.text_box_cursor = TextBox((1450, 330), (100, 40), 2, str(self.cursor_size))

        self.text_box_fps = TextBox((1450, 400), (100, 40), 3, str(Settings.FPS))

        initialize_nest()


    def reset_simulation(self):
        self.reset_grid()
        self.reset_ants()

    def reset_grid(self):
        for row in grid:
            for cell in row:
                cell["food"] = 0
                cell["obstacle"] = False
                cell["nest"] = False
              
        # Reinitialize the nest
        initialize_nest()

    def reset_ants(self):
        # Find all cells that contain a nest
        nest_cells = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x]["nest"]:
                    nest_cells.append((x, y))  # Store the coordinates of nest cells

        # If there are no nest cells, use the default nest position
        if not nest_cells:
            self.ants = []
            return

        # Reset ants to random nest cells
        self.ants = []
        for _ in range(self.num_ants):
            x, y = random.choice(nest_cells)  # Randomly select a nest cell
            self.ants.append(Ant(x, y))  # Create an ant at the selected nest cell

        # Reset pheromones
        for row in grid:
            for cell in row:
                if cell["nest"] == False or cell["food"] <= 0:
                cell["pheromone"].pheromone_food = 0
                cell["pheromone"].pheromone_home = 0
        

    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button pressed
                    self.mouse1_dragging = True
                elif event.button == 3:
                    self.mouse3_dragging = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button pressed
                    self.mouse1_dragging = False
                elif event.button == 3:
                    self.mouse3_dragging = False
                
            if event.type == pygame.MOUSEMOTION:
                if self.mouse1_dragging:
                    self.place_item(event.pos)
                elif self.mouse3_dragging:
                    self.delete_item(event.pos)

            if self.button_reset.is_clicked(event):
                self.reset_simulation()
            
            if self.button_reset_ants.is_clicked(event):
                self.reset_ants()
                
            if self.button_pause.is_clicked(event):
                self.paused = not self.paused
                self.button_pause.update_text("Pause" if not self.paused else "Play")
                
            if self.button_food.is_clicked(event):
                self.placing_food = True
                self.placing_obstacle = False
                self.placing_nest = False

            if self.button_obstacle.is_clicked(event):
                self.placing_obstacle = True
                self.placing_food = False
                self.placing_nest = False
            
            if self.button_nest.is_clicked(event):
                self.placing_nest = True
                self.placing_food = False
                self.placing_obstacle = False
            
            self.text_box_cursor.is_clicked(event)
            self.text_box_cursor.handle_event(event)
            try:
                self.cursor_size = max(0, int(self.text_box_cursor.text))
            except ValueError:
                pass  # Ignore invalid input (non-integer values)

            self.text_box_ants.is_clicked(event)  # Activate/deactivate text box
            self.text_box_ants.handle_event(event)  # Handle text input
            try:
                    self.num_ants = int(self.text_box_ants.text)
            except ValueError:
                pass  # Ignore invalid input (non-integer values)

            self.text_box_fps.is_clicked(event)  # Activate/deactivate text box
            self.text_box_fps.handle_event(event)  # Handle text input
            try:
                    self.settings.FPS = int(self.text_box_fps.text)
            except ValueError:
                pass  # Ignore invalid input (non-integer values)

    def place_item(self, pos):
        # Get the mouse position
        mouse_x, mouse_y = pos
        # Calculate the grid position
        grid_x = mouse_x // self.settings.CELL_SIZE
        grid_y = mouse_y // self.settings.CELL_SIZE

        # Calculate the start and end positions for the item placement
        start_x = max(0, grid_x - self.cursor_size // 2)
        start_y = max(0, grid_y - self.cursor_size // 2)
        end_x = min(len(grid[0]) - 1, start_x + self.cursor_size - 1)
        end_y = min(len(grid) - 1, start_y + self.cursor_size - 1)

         # Place items in the calculated area
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if self.placing_food:
                    grid[y][x]["food"] += self.settings.FOOD_NUM
                    grid[y][x]["pheromone"].deposit_food_pheromone(255)
                elif self.placing_obstacle:
                    grid[y][x]["obstacle"] = True
                elif self.placing_nest:
                    grid[y][x]["nest"] = True
                    grid[y][x]["pheromone"].deposit_home_pheromone(255)

    def delete_item(self, pos):
        # Get the mouse position
        mouse_x, mouse_y = pos
        # Calculate the grid position
        grid_x = mouse_x // self.settings.CELL_SIZE
        grid_y = mouse_y // self.settings.CELL_SIZE

        # Calculate the start and end positions for the item deletion
        start_x = max(0, grid_x - self.cursor_size // 2)
        start_y = max(0, grid_y - self.cursor_size // 2)
        end_x = min(len(grid[0]) - 1, start_x + self.cursor_size - 1)
        end_y = min(len(grid) - 1, start_y + self.cursor_size - 1)

        # Delete items in the calculated area
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if  self.placing_food:
                    # Remove food on the grid square
                    grid[y][x]["food"] -= Settings.FOOD_NUM
                    grid[y][x]["pheromone"].clear_pheromone()
                if  self.placing_obstacle:
                    grid[y][x]["obstacle"] = False
                if self.placing_nest:
                    grid[y][x]["nest"] = False
                    grid[y][x]["pheromone"].clear_pheromone()

    def update_ants(self):
        food_collected_count = 0

        for ant in self.ants:
            ant.move()
            ant.deposit_pheromone(grid)
            ant.change_state(grid)
            food_collected_count += ant.food_collected_count

        return food_collected_count


    def run(self):
        while self.running:
            self.handle_event()

            self.screen.fill("White")

            if not self.paused:
                food_collected_count = self.update_ants()
                update_pheromones()

            draw_grid(self.screen)
            draw_ants(self.screen, self.ants)

            # Draw elements of GUI

            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((1280, 0), (500, 920)))
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((0, 720), (1280, 200)))

            self.button_pause.draw(self.screen)
            self.button_reset_ants.draw(self.screen)
            self.button_reset.draw(self.screen)
            self.button_food.draw(self.screen)
            self.button_obstacle.draw(self.screen)
            self.button_nest.draw(self.screen)

            text_ants = self.font.render(f"num of ants:", True, (0, 0, 0))
            self.screen.blit(text_ants, (1320, 250))
            self.text_box_ants.draw(self.screen)
            
            text_cursor = self.font.render(f"cursor size:", True, (0, 0, 0))
            self.screen.blit(text_cursor, (1320, 350))
            self.text_box_cursor.draw(self.screen)

            text_fps = self.font.render(f"FPS:", True, (0, 0, 0))
            self.screen.blit(text_fps, (1320, 450))
            self.text_box_fps.draw(self.screen)

            text_food = self.font.render(f"food collected: {food_collected_count}", True, (0, 0, 0))
            self.screen.blit(text_food, (10, 750))
            

            # flip() the display to put your work on screen
            pygame.display.flip() 
            self.clock.tick(self.settings.FPS)  # sets FPS limit
        
        pygame.quit()




if __name__ == "__main__":
    sim = Simulation()
    sim.run()
