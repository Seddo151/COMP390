class Settings:

    SCREEN_HEIGHT = 920
    SCREEN_WIDTH = 1780
    FPS = 100 # determines how many times a second grid is updated etc

    SIM_HEIGHT = 720
    SIM_WIDTH = 1280
    CELL_SIZE = 4 # Pixels per square
    GRID_ROWS = (SIM_HEIGHT // CELL_SIZE) -1 # num of rows in grid
    GRID_COLUMNS = (SIM_WIDTH // CELL_SIZE) - 1 # mum of columns in grid

    TOTAL_ANTS = 1000
    ANT_MEMORY_SIZE = 20 # how many previous cells the ant wont re-visit
    PHEROMONE_DECAY_RATE = 0.01 # speed that pheromones decay

    NEST_POS_X = 70
    NEST_POS_Y = 70

    FOOD_NUM = 1000 # food available on a placed food cell



    #to add

        # obstacle layer around edge once obstacle avoidence has been implemented