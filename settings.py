class Settings:

    SCREEN_HEIGHT = 920
    SCREEN_WIDTH = 1780
    FPS = 60 # determines how many times a second grid is updated etc

    SIM_HEIGHT = 720
    SIM_WIDTH = 1280
    CELL_SIZE = 4 # Pixels per square
    GRID_ROWS = (SIM_HEIGHT // CELL_SIZE) -1 # num of rows in grid
    GRID_COLUMNS = (SIM_WIDTH // CELL_SIZE) - 1 # mum of columns in grid

    DEFAULT_NUM_ANTS = 0
    ANT_MEMORY_SIZE = 40 # how many previous cells the ant wont re-visit
    DECAY_RATE_FOOD = 0.01 # speed that pheromones decay
    DECAY_RATE_HOME = 0.01

    FOOD_NUM = 100 # food available on a placed food cell

    PHEROMONE_DIFFUSION_RATE = 0.01
   