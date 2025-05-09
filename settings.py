class Settings:
    SCREEN_HEIGHT = 920 # Height of the window
    SCREEN_WIDTH = 1780 # Width of the window

    FPS = 30 # determines how many times a second the main loop is run

    SIM_HEIGHT = 720 # Height of the simulation space
    SIM_WIDTH = 1280 # Width of the simulation space
    CELL_SIZE = 6 # Size of a cell in the grid
    GRID_ROWS = (SIM_HEIGHT // CELL_SIZE) # Num of rows in the grid
    GRID_COLUMNS = (SIM_WIDTH // CELL_SIZE) # Num of columns in the grid

    DEFAULT_NUM_ANTS = 500 # Default number of ants in a colony
    ANT_MEMORY_SIZE = 40 # Amount of the last visited cells remembered by the ant
    DECAY_RATE_FOOD = 0.01 # Decay rate of the food pheromones
    DECAY_RATE_HOME = 0.01 # Decay rate of the home pheromones

    FOOD_NUM = 50 # Value of the food placed in a cell

    PHEROMONE_DIFFUSION_RATE = 0.01 # Rate of pheromone diffusion
   