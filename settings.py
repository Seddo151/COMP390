class Settings:

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 100 # determines how many times a second grid is updated etc

    CELL_SIZE = 4 # Pixels per square
    GRID_ROWS = (SCREEN_HEIGHT // CELL_SIZE) -1 # num of rows in grid
    GRID_COLUMNS = (SCREEN_WIDTH // CELL_SIZE) - 1 # mum of columns in grid

    TOTAL_ANTS = 1000
    ANT_MEMORY_SIZE = 20 # how many previous cells the ant wont re-visit
    PHEROMONE_DECAY_RATE = 0.1 # speed that pheromones decay

    NEST_POS_X = 70
    NEST_POS_Y = 70

    FOOD_NUM = 1000 # food available on a placed food cell