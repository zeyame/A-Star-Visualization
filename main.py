import pygame
import math
from queue import PriorityQueue

# setting up our window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# setting the caption 
pygame.display.set_caption("A* Path Finding Algorithm")

# setting up our colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# class representing a grid cell 
class Spot:
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width        # x coordinate
        self.y = col * width        # y coordinate
        self.color = WHITE
        self.neighbors = []         # adjacent spots
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
        
    def make_start(self):
        self.color = ORANGE
        
    def make_closed(self):
        self.color = RED
        
    def make_opened(self):
        self.color = GREEN
        
    def make_barrier(self):
        self.color = BLACK
        
    def make_end(self):
        self.color = TURQUOISE
        
    def make_path(self):
        self.color = PURPLE
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    # method updates the neighbors of a spot which can be used as an edge (not a barrier)
    def update_neighbors(self, grid):
        self.neighbors = []
        
        #UP
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
            
        #DOWN
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])                           
            
        #LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
            
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col+1])                           
            
        
    
    def __lt__(self, other):
        return False
    
# The Manhattan distance will be used to calculate the heuristic value of a node to the end node
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Method used to retrace the nodes/spots traversed from the start node to the end node
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current.make_path()
        current = came_from[current]
        draw()  # draw is passed as a function to this function's parameter 


# A* algorithm implementation
def a_star(draw, grid, start, end):
    count = 0  
    open_set = PriorityQueue()
    open_set.put((h(start.get_pos(), end.get_pos()), count, start))
    came_from = {}  # dict to store the previous node for every traversed node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}     # a set to store the spot objects yet to be explored
    
    while not open_set.empty():
        # if user quits mid algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]     # retrieving the lowest f score spot from the queue 
        open_set_hash.remove(current)   # removing the spot from the set 
        
        # arrived at the target end node
        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()      # making end spot visible from rest of path
            return True
        
        # exploring neighbors of current spot
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1     # assuming the edge to go to any spot/node costs 1 
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_opened()
        
        draw()
        
        # once we explore the neighbors of a node, we have visited this current node and we close it
        if current != start:
            current.make_closed()
            
    return False
                    
    

# Creating the grid storing the spots using a 2D array
def create_grid(rows, width):
    grid = []   # 2D array to store spots of grid
    gap = width // rows     # This will determine how wide each square spot will be
    
    # making a sublist for every row of our grid
    for i in range(rows):
        grid.append([])
        # adding the spots to every row
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid


# method is responsible for drawing the grid lines only
def draw_grid(win, rows, width):
    gap = width // rows
    
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, gap * i), (width, gap * i))     # horizontal lines
        
        for j in range(rows):
            pygame.draw.line(win, GREY, (gap * j, 0), (gap * j, width))     # vertical lines
            
            
def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    # drawing the spots on our grid
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    # drawing the grid lines 
    draw_grid(win, rows, width)
    
    # displaying the updates to the window
    pygame.display.update()
    

# Method takes in the coordinates of a mouse click and returns the row and column position on the grid
def get_clicked_pos(pos, width, rows):
    gap = width // rows
    y , x = pos
    
    row = y // gap      # row of the spot clicked
    col = x // gap      # column of the spot clicked
    
    return row, col


# Method that will execute the program
def main(win , width):
    ROWS = 50
    grid = create_grid(ROWS, width)
    
    # variables indicating the start and end spots on the grid
    start = None
    end = None
    
    run = True      # whether the game is running 
    
    while run:
        draw(win, grid, ROWS, width)    # drawing the empty grid
        
        for event in pygame.event.get():
            # if user presses the quit button
            if event.type == pygame.QUIT:
                run = False
                break
            
            # handling the left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()    # getting the coordinates of the click
                row, col = get_clicked_pos(pos, width, ROWS)    # getting row, column position of the click
                spot = grid[row][col]       # retrieving the specific spot clicked
                
                # we always assign the first spot clicked to be the start point as long as it is not the same spot as the end point
                if not start and spot != end:
                    start = spot
                    start.make_start()
                
                # we then assign the second spot clicked to be the end point as long as it is not the same spot as the start point
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                # if start and end have been assigned, we make the spot a barrier as long as it is different from the start and end spots
                elif spot != start and spot != end:
                    spot = grid[row][col]
                    spot.make_barrier()
            
            # handling the right mouse button
            elif pygame.mouse.get_pressed()[2]:
                # same code as the left mouse click
                pos = pygame.mouse.get_pos() 
                row, col = get_clicked_pos(pos, width, ROWS)
                spot = grid[row][col]
                spot.reset()        # spot reverts to a white spot
                
                # in order to be able to re-assign start and end spots to the grid again
                if spot == start:
                    start = None
                
                elif spot == end:
                    end = None
            
            # handling some keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:   # user presses space bar and assigned start and end nodes
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    # calling the A* algorithm once all spots have been assigned their neighbors
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # event for clearing the window without shutting off the program
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)
    
    # quitting the program once loop exits
    pygame.quit()
                    
                    
main(WIN, WIDTH)
                
    
    


    