import pygame
import cProfile
from settings import Settings
from grid import Grid
from gui import Button, TextBox 
from colony import Colony

GARDEN_ANT = ((0,0,0), # colour
               (0.1, 0.9, 0.1), # random vals
                 5.0, # directionality
                   False) # deposition depenedent on food size
CRAZY_ANT = ((255,0,0), (0.4, 0.9, 0.1), 4.0, False)
ARGENTINE_ANT = ((200,100,0), (0.15, 0.9, 0.1), 5.0, True)
PHARAOH_ANT = ((0,0,255), (0.15, 0.9, 0.1), 10.0, False)

SPECIES = [GARDEN_ANT, CRAZY_ANT, ARGENTINE_ANT, PHARAOH_ANT]

class Simulation:
    def __init__(self):

        pygame.init()

        self.settings = Settings()
        self.running = True
        self.paused = True

        self.cursor_size = 4 # Size of what the user is modifying on the grid
        self.modify_state = 'food' # What element the user is modifying on the grid

        self.mouse1_dragging = False # Flag for if left mouse button is pressed and mouse is moved
        self.mouse3_dragging = False # Flag for if right mouse button is pressed and mouse is moved

        self.colonies = (Colony(GARDEN_ANT, 0),
                         Colony(GARDEN_ANT, 1),
                         Colony(GARDEN_ANT, 2),
                         Colony(GARDEN_ANT, 3)) # Initialised the colonies
        
        self.selected_nest_index = 0 # Which nest is being moved in simulation area
        self.grid = Grid() # Creates the grid

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24) 
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Ant Colony Simulation")

        self.create_gui() # Declares GUI elements

    # Resets everything in the simulation area
    def reset_simulation(self):
        self.grid.clear_grid() # Clears the grid
        self.reset_ants() # Resets the ants
        self.colonies = (Colony(self.colonies[0].species, 0),
                         Colony(self.colonies[1].species, 1),
                         Colony(self.colonies[2].species, 2),
                         Colony(self.colonies[3].species, 3)) # Re-initalises the colonies

    # Resets the ants and pheromones in the simulation area
    def reset_ants(self):
        # Resets the ants in each colony
        for col in self.colonies:
            col.reset_ants(self.grid)

        self.grid.clear_pheromones() # Clears the pheromones from the grid
        

    # Handles all the user interactions with the GUI
    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button pressed
                    self.mouse1_dragging = True
                elif event.button == 3: # Right mouse button pressed
                    self.mouse3_dragging = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    self.mouse1_dragging = False
                elif event.button == 3: # Right mouse button released
                    self.mouse3_dragging = False

            # Determines what should be modified in the simulation area
            # Left mouse button places objects and Right mouse deletes
            if event.type == pygame.MOUSEMOTION:
                if self.modify_state == 'nest' and self.mouse1_dragging:
                    self.colonies[self.selected_nest_index].move_nest(self.grid, event.pos)
                elif self.mouse1_dragging:
                    self.grid.modify_item(event.pos,'place', self.cursor_size, self.modify_state)
                elif self.mouse3_dragging:
                    self.grid.modify_item(event.pos,'delete', self.cursor_size, self.modify_state)


            if self.button_reset.is_clicked(event):
                self.reset_simulation()
            
            if self.button_reset_ants.is_clicked(event):
                self.reset_ants()
                
            if self.button_pause.is_clicked(event):
                self.paused = not self.paused
                self.button_pause.update_text("Pause" if not self.paused else "Play")
                
            if self.button_food.is_clicked(event):
                self.modify_state = 'food'

            if self.button_obstacle.is_clicked(event):
                self.modify_state = 'obstacle'
            
            if self.button_nest_1.is_clicked(event):
                self.modify_state = 'nest'
                self.selected_nest_index = 0

            if self.button_nest_2.is_clicked(event):
                self.modify_state = 'nest'
                self.selected_nest_index = 1
            
            if self.button_nest_3.is_clicked(event):
                self.modify_state = 'nest'
                self.selected_nest_index = 2

            if self.button_nest_4.is_clicked(event):
                self.modify_state = 'nest'
                self.selected_nest_index = 3


            for i, buttons in enumerate(self.species_button_groups):
                for j, button in enumerate(buttons):
                    if button.is_clicked(event):
                        self.colonies[i].species = SPECIES[j]

            # Handles textbox input to determine size of modifying area
            self.textbox_cursor.is_clicked(event)
            self.textbox_cursor.handle_event(event)
            try:
                self.cursor_size = max(0, int(self.textbox_cursor.text))
            except ValueError:
                pass  # Ignores none integer values

            # Handles textbox input to determine num of ants in colony 1
            self.textbox_ants_1.is_clicked(event)  
            self.textbox_ants_1.handle_event(event)  
            try:
                    self.colonies[0].num_ants = int(self.textbox_ants_1.text)
            except ValueError:
                pass  # Ignores none integer values

            # Handles textbox input to determine num of ants in colony 2
            self.textbox_ants_2.is_clicked(event)  
            self.textbox_ants_2.handle_event(event)  
            try:
                    self.colonies[1].num_ants = int(self.textbox_ants_2.text)
            except ValueError:
                pass  # Ignores none integer values

            # Handles textbox input to determine num of ants in colony 3
            self.textbox_ants_3.is_clicked(event)  
            self.textbox_ants_3.handle_event(event)  
            try:
                    self.colonies[2].num_ants = int(self.textbox_ants_3.text)
            except ValueError:
                pass  # Ignores none integer values

            # Handles textbox input to determine num of ants in colony 4
            self.textbox_ants_4.is_clicked(event)  
            self.textbox_ants_4.handle_event(event)  
            try:
                    self.colonies[3].num_ants = int(self.textbox_ants_4.text)
            except ValueError:
                pass  # Ignores none integer values

            # Handles textbox input to determine fps of simulation 
            self.textbox_fps.is_clicked(event) 
            self.textbox_fps.handle_event(event)  
            try:
                    self.settings.FPS = int(self.textbox_fps.text)
            except ValueError:
                pass  # Ignores none integer values


    # Declares all the element of the GUI
    def create_gui(self):
        self.button_pause = Button("Play", (10, 750), (100, 50))
        self.button_reset = Button("Reset", (10, 850), (100, 50))

        self.button_food = Button("Food", (210, 750), (100, 50))
        self.button_obstacle = Button("Obstacle", (410, 750), (100, 50))
        self.button_reset_ants = Button("Reset Ants", (1150, 750), (100, 50))
        self.textbox_cursor = TextBox((410, 850), (100, 40), 2, str(self.cursor_size))
        self.textbox_fps = TextBox((750, 850), (100, 40), 3, str(self.settings.FPS))

        self.button_nest_1 = Button("Nest", (1300, 50), (50, 50))
        self.textbox_ants_1 = TextBox((1300, 150), (50, 40), 4, str(self.colonies[0].num_ants))
        self.buttons_species_1 = [Button("Garden Ant", (1290, 250), (110, 50)),
                                Button("Crazy Ant", (1290, 330), (110, 50)),
                                Button("Argentine Ant", (1290, 410), (110, 50)),
                                Button("Pharaoh Ant", (1290, 490), (110, 50))]

        self.button_nest_2 = Button("Nest", (1425, 50), (50, 50))
        self.textbox_ants_2 = TextBox((1425, 150), (50, 40), 4, str(self.colonies[1].num_ants))
        self.buttons_species_2 = [Button("Garden Ant", (1415, 250), (110, 50)),
                                Button("Crazy Ant", (1415, 330), (110, 50)),
                                Button("Argentine Ant", (1415, 410), (110, 50)),
                                Button("Pharaoh Ant", (1415, 490), (110, 50))]

        self.button_nest_3 = Button("Nest", (1550, 50), (50, 50))
        self.textbox_ants_3 = TextBox((1550, 150), (50, 40), 4, str(self.colonies[2].num_ants))
        self.buttons_species_3 = [Button("Garden Ant", (1540, 250), (110, 50)),
                                Button("Crazy Ant", (1540, 330), (110, 50)),
                                Button("Argentine Ant", (1540, 410), (110, 50)),
                                Button("Pharaoh Ant", (1540, 490), (110, 50))]

        self.button_nest_4 = Button("Nest", (1675, 50), (50, 50))
        self.textbox_ants_4 = TextBox((1675, 150), (50, 40), 4, str(self.colonies[3].num_ants))
        self.buttons_species_4 = [Button("Garden Ant", (1665, 250), (110, 50)),
                                Button("Crazy Ant", (1665, 330), (110, 50)),
                                Button("Argentine Ant", (1665, 410), (110, 50)),
                                Button("Pharaoh Ant", (1665, 490), (110, 50))]

        self.species_button_groups = [
                self.buttons_species_1,
                self.buttons_species_2,
                self.buttons_species_3,
                self.buttons_species_4,
            ]

    # Draws all of the elements of the GUI
    def draw_gui(self):
            
            self.button_food.active = (self.modify_state == 'food')
            self.button_obstacle.active = (self.modify_state == 'obstacle')
            self.button_nest_1.active = True if (self.modify_state == 'nest' and self.selected_nest_index == 0) else False
            self.button_nest_2.active = True if (self.modify_state == 'nest' and self.selected_nest_index == 1) else False
            self.button_nest_3.active = True if (self.modify_state == 'nest' and self.selected_nest_index == 2) else False
            self.button_nest_4.active = True if (self.modify_state == 'nest' and self.selected_nest_index == 3) else False

            for i, buttons in enumerate(self.species_button_groups):
                for j, button in enumerate(buttons):
                    button.active = self.colonies[i].species == SPECIES[j]
                    
        
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((1280, 0), (500, 920)))
            pygame.draw.rect(self.screen, (200, 200, 200) , pygame.Rect((0, 720), (1280, 200)))

            self.button_pause.draw(self.screen)
            self.button_reset_ants.draw(self.screen)
            self.button_reset.draw(self.screen)
            self.button_food.draw(self.screen)
            self.button_obstacle.draw(self.screen)

            self.button_nest_1.draw(self.screen)
            self.screen.blit(self.font.render(f"ants num:", True, (0, 0, 0)), (1300, 130))
            self.textbox_ants_1.draw(self.screen)
            self.buttons_species_1[0].draw(self.screen)
            self.buttons_species_1[1].draw(self.screen)
            self.buttons_species_1[2].draw(self.screen)
            self.buttons_species_1[3].draw(self.screen)

            self.button_nest_2.draw(self.screen)
            self.screen.blit(self.font.render(f"ants num:", True, (0, 0, 0)), (1425, 130))
            self.textbox_ants_2.draw(self.screen)
            self.buttons_species_2[0].draw(self.screen)
            self.buttons_species_2[1].draw(self.screen)
            self.buttons_species_2[2].draw(self.screen)
            self.buttons_species_2[3].draw(self.screen)

            self.button_nest_3.draw(self.screen)
            self.screen.blit(self.font.render(f"ants num:", True, (0, 0, 0)), (1550, 130))
            self.textbox_ants_3.draw(self.screen)
            self.buttons_species_3[0].draw(self.screen)
            self.buttons_species_3[1].draw(self.screen)
            self.buttons_species_3[2].draw(self.screen)
            self.buttons_species_3[3].draw(self.screen)

            self.button_nest_4.draw(self.screen)
            self.screen.blit(self.font.render(f"ants num:", True, (0, 0, 0)), (1675, 130))
            self.textbox_ants_4.draw(self.screen)
            self.buttons_species_4[0].draw(self.screen)
            self.buttons_species_4[1].draw(self.screen)
            self.buttons_species_4[2].draw(self.screen)
            self.buttons_species_4[3].draw(self.screen)
            
            self.screen.blit(self.font.render(f"cursor size:", True, (0, 0, 0)), (310, 860))
            self.textbox_cursor.draw(self.screen)

            self.screen.blit(self.font.render(f"FPS:", True, (0, 0, 0)), (700, 860))
            self.textbox_fps.draw(self.screen)

            text_food = self.font.render(f"Colony1 food: {self.colonies[0].food_collected}" , True, (0, 0, 0))
            self.screen.blit(text_food, (1300, 575))

            text_food = self.font.render(f"Colony2 food: {self.colonies[1].food_collected}" , True, (0, 0, 0))
            self.screen.blit(text_food, (1300, 610))

            text_food = self.font.render(f"Colony3 food: {self.colonies[2].food_collected}" , True, (0, 0, 0))
            self.screen.blit(text_food, (1300, 645))

            text_food = self.font.render(f"Colony4 food: {self.colonies[3].food_collected}" , True, (0, 0, 0))
            self.screen.blit(text_food, (1300, 680))

            self.screen.blit(self.font.render(f"Colony 1", True, (0, 0, 0)), (1300, 20))
            self.screen.blit(self.font.render(f"Colony 2", True, (0, 0, 0)), (1425, 20))
            self.screen.blit(self.font.render(f"Colony 3", True, (0, 0, 0)), (1550, 20))
            self.screen.blit(self.font.render(f"Colony 4", True, (0, 0, 0)), (1675, 20))        

            self.screen.blit(self.font.render(f"Species:", True, (0, 0, 0)), (1300, 220))
            self.screen.blit(self.font.render(f"Species:", True, (0, 0, 0)), (1425, 220))
            self.screen.blit(self.font.render(f"Species:", True, (0, 0, 0)), (1550, 220))
            self.screen.blit(self.font.render(f"Species:", True, (0, 0, 0)), (1675, 220))


    def run(self):
        # Main loop
        while self.running:
            self.handle_event() # Handles user interactions

            self.screen.fill("White") # Sets background of screen 

            if not self.paused:
                for col in self.colonies:
                    col.update_ants(self.grid) # Updates ant movement, pheromone deposition etc
                self.grid.decay_pheromones() # Decays pheromones

            self.grid.draw_grid(self.screen) # Draws the updated grid to the screen

            # Draws each of the ants
            for col in self.colonies:
                self.grid.draw_ants(self.screen, col.ants, col.species[0])
        
            self.draw_gui() # Draws the GUI

            pygame.display.flip() 
            self.clock.tick(self.settings.FPS)  # sets the FPS limit
        pygame.quit()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    #cProfile.run('sim.run()', sort='cumulative')
