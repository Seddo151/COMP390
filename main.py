import pygame
from settings import Settings
from draw import draw_grid, draw_ants
from ant import Ant
from grid import grid, initialize_nest, update_pheromones
from gui import Button, TextBox

class Simulation:
    def __init__(self):

        pygame.init()

        self.settings = Settings()
        self.running = True
        self.paused = False
        self.placing_food = True
        self.placing_obstacle = False
        self.placing_nest = False
        self.mouse1_dragging = False
        self.mouse3_dragging = False
        self.ants = [Ant(Settings.NEST_POS_X, Settings.NEST_POS_Y) for _ in range(Settings.TOTAL_ANTS)]

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Ant Colony Simulation")

        # Create GUI elements
        self.button_play = Button("Play", (1320, 40), (100, 50))
        self.button_pause = Button("Pause", (1490, 40), (100, 50))
        self.button_reset = Button("Reset", (1650, 40), (100, 50))
        self.button_food = Button("Food", (1320, 120), (100, 50))
        self.button_obstacle = Button("Obstacle", (1490, 120), (100, 50))
        self.button_nest = Button("Nest", (1650, 120), (100, 50))
        self.text_box = TextBox((1000, 200), (200, 40))

        initialize_nest()


    def reset_simulation(self):
        self.reset_grid()
        self.reset_ants()

    def reset_grid(self):
        for row in grid:
            for cell in row:
                cell["food"] = 0
                cell["obstacle"] = False
                cell["pheromone"].pheromone_food = 0
                cell["pheromone"].pheromone_home = 0
        # Reinitialize the nest
        initialize_nest()

    def reset_ants(self):
        for ant in self.ants:
            ant.x = self.settings.NEST_POS_X
            ant.y = self.settings.NEST_POS_Y
            ant.has_food = False
            ant.visited_positions = []
            ant.last_direction = (0, 0)
            ant.returning_timer = 0
            ant.food_collected_count = 0


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

            if self.button_play.is_clicked(event):
                self.paused = False
                
            if self.button_pause.is_clicked(event):
                self.paused = True
            
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
    
    def place_item(self, pos):
        # Get the mouse position
        mouse_x, mouse_y = pos
        # Calculate the grid position
        grid_x = mouse_x // self.settings.CELL_SIZE
        grid_y = mouse_y // self.settings.CELL_SIZE

        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if  self.placing_food:
                # Place food on the grid square
                grid[grid_y][grid_x]["food"] += Settings.FOOD_NUM
                grid[grid_y][grid_x]["pheromone"].deposit_food_pheromone(255)
            if  self.placing_obstacle:
                grid[grid_y][grid_x]["obstacle"] = True
            if self.placing_nest:
                grid[grid_y][grid_x]["nest"] = True
                grid[grid_y][grid_x]["pheromone"].deposit_home_pheromone(255)

    def delete_item(self, pos):
        # Get the mouse position
        mouse_x, mouse_y = pos
        # Calculate the grid position
        grid_x = mouse_x // self.settings.CELL_SIZE
        grid_y = mouse_y // self.settings.CELL_SIZE

        if 0 <= grid_x < len(grid[0]) and 0 <= grid_y < len(grid):
            if  self.placing_food:
                # Remove food on the grid square
                grid[grid_y][grid_x]["food"] -= Settings.FOOD_NUM
                grid[grid_y][grid_x]["pheromone"].clear_pheromone()
            if  self.placing_obstacle:
                grid[grid_y][grid_x]["obstacle"] = False
            if self.placing_nest:
                grid[grid_y][grid_x]["nest"] = False
                grid[grid_y][grid_x]["pheromone"].clear_pheromone()

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

            # Draw elements of gui
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((1280, 0), (500, 920)))
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((0, 720), (1280, 200)))
            self.button_play.draw(self.screen)
            self.button_pause.draw(self.screen)
            self.button_reset.draw(self.screen)
            self.button_food.draw(self.screen)
            self.button_obstacle.draw(self.screen)
            self.button_nest.draw(self.screen)
            self.text_box.draw(self.screen)
            
            text = self.font.render(f"food collected: {food_collected_count}", True, (0, 0, 0))
            self.screen.blit(text, (10, 750))

            # flip() the display to put your work on screen
            pygame.display.flip() 
            self.clock.tick(self.settings.FPS)  # limits FPS to 60
        
        pygame.quit()




if __name__ == "__main__":
    sim = Simulation()
    sim.run()