import pygame
import cProfile
from settings import Settings
from grid import Grid
from gui import Button, TextBox
from colony import Colony

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

        self.colonys = [Colony()]
        self.grid = Grid()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Ant Colony Simulation")

        # Create GUI elements
        self.button_pause = Button("Pause", (10, 750), (100, 50))
        self.button_reset = Button("Reset", (10, 850), (100, 50))

        self.button_food = Button("Food", (210, 750), (100, 50))
        self.button_obstacle = Button("Obstacle", (410, 750), (100, 50))
        self.button_nest = Button("Nest", (1300, 50), (50, 50))

        self.text_box_ants = TextBox((1300, 150), (50, 40), 4, str(self.colonys[0].num_ants))
        self.button_reset_ants = Button("Reset Ants", (1150, 750), (100, 50))
        
        self.text_box_cursor = TextBox((410, 850), (100, 40), 2, str(self.cursor_size))

        self.text_box_fps = TextBox((750, 850), (100, 40), 3, str(Settings.FPS))


    def reset_simulation(self):
        self.grid.reset_grid()
        self.reset_ants()


    def reset_ants(self):
        
        for col in self.colonys:
            col.reset_ants()

        self.grid.reset_pheromones()
        

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
                    self.modify_item(event.pos,'place')
                elif self.mouse3_dragging:
                    self.modify_item(event.pos,'delete')

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
                    self.colonys[0].num_ants = int(self.text_box_ants.text)
            except ValueError:
                pass  # Ignore invalid input (non-integer values)

            self.text_box_fps.is_clicked(event)  # Activate/deactivate text box
            self.text_box_fps.handle_event(event)  # Handle text input
            try:
                    self.settings.FPS = int(self.text_box_fps.text)
            except ValueError:
                pass  # Ignore invalid input (non-integer values)

    def modify_item(self, pos, action):
        grid = self.grid.grid
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
                if action == 'place':
                    if self.placing_food:
                        grid[y][x]["food"] += self.settings.FOOD_NUM
                        grid[y][x]["pheromone"].deposit_food_pheromone(255)
                    elif self.placing_obstacle:
                        grid[y][x]["obstacle"] = True
                    elif self.placing_nest:
                        # Ensure only one nest per colony
                        for col in self.colonys:
                            col.place_nest(grid, x, y)
                elif action == 'delete':
                    if  self.placing_food:
                        # Remove food on the grid square
                        grid[y][x]["food"] -= self.settings.FOOD_NUM
                        grid[y][x]["pheromone"].clear_pheromone()
                    if  self.placing_obstacle:
                        grid[y][x]["obstacle"] = False
                    if self.placing_nest:
                        grid[y][x]["nest"] = False
                        grid[y][x]["pheromone"].clear_pheromone()
        
 
    def draw_gui(self):
        # Draw elements of GUI

            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((1280, 0), (500, 920)))
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((0, 720), (1280, 200)))

            self.button_pause.draw(self.screen)
            self.button_reset_ants.draw(self.screen)
            self.button_reset.draw(self.screen)
            self.button_food.draw(self.screen)
            self.button_obstacle.draw(self.screen)
            self.button_nest.draw(self.screen)

            self.screen.blit(self.font.render(f"ants num:", True, (0, 0, 0)), (1300, 130))
            self.text_box_ants.draw(self.screen)
            
            self.screen.blit(self.font.render(f"cursor size:", True, (0, 0, 0)), (310, 860))
            self.text_box_cursor.draw(self.screen)

            self.screen.blit(self.font.render(f"FPS:", True, (0, 0, 0)), (700, 860))
            self.text_box_fps.draw(self.screen)

            text_food = self.font.render(f"food collected: {self.colonys[0].food_collected}" , True, (0, 0, 0))
            self.screen.blit(text_food, (1300, 600))

            self.screen.blit(self.font.render(f"Colony 1", True, (0, 0, 0)), (1300, 20))
            self.screen.blit(self.font.render(f"Colony 2", True, (0, 0, 0)), (1425, 20))
            self.screen.blit(self.font.render(f"Colony 3", True, (0, 0, 0)), (1550, 20))
            self.screen.blit(self.font.render(f"Colony 4", True, (0, 0, 0)), (1675, 20))        

            self.screen.blit(self.font.render(f"Species:", True, (0, 0, 0)), (1300, 220))


    


    def run(self):
        while self.running:
            self.handle_event()

            self.screen.fill("White")

            if not self.paused:
                for col in self.colonys:
                    col.update_ants(self.grid)
                self.grid.update_pheromones()

            self.grid.draw_grid(self.screen)

            for col in self.colonys:
                self.grid.draw_ants(self.screen, col.ants)
        

            self.draw_gui()

            
            pygame.display.flip() 
            self.clock.tick(self.settings.FPS)  # sets FPS limit
        
        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    # cProfile.run('sim.run()', sort='cumulative')
