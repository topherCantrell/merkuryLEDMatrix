
import random

# Up, Right, Down, Left
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Cells to check for a clear path. This keeps rooms from being diagonally adjacent.
CHECK_FOR_DIR = [
    [(-1,0),  (1,0),  (-1,-1), (0,-1), (1,-1)], # Moving up
    [(0,-1), (0,1),   (1,-1), (1,0), (1,1)],    # Moving right
    [(-1,0), (1,0),   (-1,1), (0,1), (1,1)],    # Moving down
    [(0,-1), (0,1),   (-1,-1), (-1,0), (-1,1)]  # Moving left
]
    
def show_ascii(pixelgrid):
    """show ascii representation for debugging"""
    for y in range(pixelgrid.height):
        for x in range(pixelgrid.width):
            if pixelgrid.get_pixel(x,y) == 0:
                print(".", end="")
            else:
                print("#", end="")
        print()

def get_empty_neighbors(pixelgrid, x, y, spots):
    """return a list of empty neighbors

    The return is an array of (i, x, y) where i is the index
    into the spots array.        
    """
    ret = []
    for i in range(len(spots)):
        dx, dy = spots[i]
        nx, ny = x + dx, y + dy
        if nx >= 0 and nx < pixelgrid.width and ny >= 0 and ny < pixelgrid.height:
            if pixelgrid.get_pixel(nx,ny) == 1:
                ret.append((i, nx, ny))
    return ret    

def generate(pixelgrid):
    """Generate a maze using Prim's algorithm"""

    pixelgrid.fill(1)  # Fill the grid with walls (1)

    # Start at a random cell
    x, y = (random.randint(0,pixelgrid.width-2-1)+1, random.randint(0,pixelgrid.height-2-1)+1)
    cells = [(x, y)]
    pixelgrid.set_pixel(x, y, 0)

    # While there are cells in the list
    while cells:
        # Pick a random cell to grow from
        n = random.randint(0, len(cells)-1)
        cx, cy = cells[n]

        # Get the free neighbors immediately adjacent
        free_neighbors = get_empty_neighbors(pixelgrid, cx, cy, DIRS)    
        available = []
        for i, nx, ny in free_neighbors:
            # For each free neighbor, check the 5 spots around it in the direction of travel
            clear_spots = get_empty_neighbors(pixelgrid, nx, ny, CHECK_FOR_DIR[i])
            if len(clear_spots)==5:
                # Five spots free ... this is a valid move
                available.append((i, nx, ny))

        # No valid moves, remove this cell from the list and continue with the next
        if not available:                
            del cells[n]        
            continue

        # Pick a random available neighbor
        _, nx, ny = available[random.randint(0, len(available)-1)]

        # Carve out this cell and add it to our growth list
        pixelgrid.set_pixel(nx, ny, 0)
        cells.append((nx, ny))
