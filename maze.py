import random
import time

import board             # Information about the GPIO pins (hardware specific)
import busio             # I2C bus library
import adafruit_mpu6050  # Accelerometer library
import neopixel          # Adafruit neopixel library

# Strand of 256 neopixels on pin GP6
neo = neopixel.NeoPixel(board.GP6, 256, auto_write=False)
neo.fill((0,0,10))
neo.show()

# MPU6050 accelerometer on an I2C bus
acc_i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(acc_i2c)

class Maze:

    # Up, Right, Down, Left
    DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # Cells to check for a clear path. This keeps rooms from being diagonally adjacent.
    CHECK_FOR_DIR = [
        [(-1,0),  (1,0),  (-1,-1), (0,-1), (1,-1)], # Moving up
        [(0,-1), (0,1),   (1,-1), (1,0), (1,1)],    # Moving right
        [(-1,0), (1,0),   (-1,1), (0,1), (1,1)],    # Moving down
        [(0,-1), (0,1),   (-1,-1), (-1,0), (-1,1)]  # Moving left
    ]

    def __init__(self, width, height):        
        self.width = width
        self.height = height        

    def fill(self, value):
        """Fill every room with the given value"""
        self.grid = [[value for x in range(self.width)] for y in range(self.height)]

    def show(self):
        """show ascii representation for debugging"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def get_empty_neighbors(self, x, y, spots):
        """return a list of empty neighbors

        The return is an array of (i, x, y) where i is the index
        into the spots array.        
        """
        ret = []
        for i in range(len(spots)):
            dx, dy = spots[i]
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                if self.grid[ny][nx] == 1:
                    ret.append((i, nx, ny))
        return ret

    def get_cell(self, x, y):
        # 2D math
        return self.grid[y][x]
    
    def set_cell(self, x, y, value):
        # 2D math
        self.grid[y][x] = value

    def generate(self):
        """Generate a maze using Prim's algorithm"""

        # Start at a random cell
        x, y = (random.randint(0,self.width-2)+1, random.randint(0,self.height-2)+1)
        cells = [(x, y)]
        self.set_cell(x, y, 0)

        # While there are cells in the list
        while cells:
            # Pick a random cell to grow from
            n = random.randint(0, len(cells)-1)
            cx, cy = cells[n]

            # Get the free neighbors immediately adjacent
            free_neighbors = self.get_empty_neighbors(cx, cy, Maze.DIRS)    
            available = []
            for i, nx, ny in free_neighbors:
                # For each free neighbor, check the 5 spots around it in the direction
                clear_spots = self.get_empty_neighbors(nx, ny, Maze.CHECK_FOR_DIR[i])
                if len(clear_spots)==5:
                    # Five spots free ... this is a valid move
                    available.append((i, nx, ny))

            # No valid moves, remove this cell from the list and continue with the next
            if not available:                
                del cells[n]        
                continue

            # Carve out this cell and add it to our growth list
            _, nx, ny = available[random.randint(0, len(available)-1)]
            self.set_cell(nx, ny, 0)
            cells.append((nx, ny))
        

def play():

    # Get a random maze wall color
    r,g,b = random.randint(0,100), random.randint(0,100), random.randint(0,100)
    m = Maze(16,16)

    # Generat a random 16x16 maze
    m.fill(1)    # Fill with walls ...
    m.generate() # ... and carve out a path through the maze

    # Copy the maze to the neopixels
    for y in range(m.height):
        for x in range(m.width):
            if m.get_cell(x, y) == 1:
                neo[y*16+x] = (r,g,b)
            else:
                neo[y*16+x] = (0,0,0)

    # Add a treasure to the maze
    treasure_x, treasure_y = random.randint(0,15), random.randint(0,15)
    while m.get_cell(treasure_x, treasure_y) != 0:
        treasure_x, treasure_y = random.randint(0,15), random.randint(0,15)
    m.set_cell(treasure_x, treasure_y, 2)
    neo[treasure_y*16+treasure_x] = (50,50,0)

    # Add the player to the maze
    player_x, player_y = random.randint(0,15), random.randint(0,15)
    while m.get_cell(player_x, player_y) != 0:
        player_x, player_y = random.randint(0,15), random.randint(0,15)
    neo[player_y*16+player_x] = (0,0,50)

    # Show the game
    neo.show()

    while True:

        # Read the accelerometer. Each axis is around -9.8 to 9.8.
        dx, dy = 0,0
        y_acc, x_acc, z_acc = mpu.acceleration
        # Simple input mapping here. If the accelerometer is tilted more than 2 units.
        if x_acc < -2:
            dx = -1
        elif x_acc > 2:
            dx = 1
        if y_acc < -2:
            dy = -1
        elif y_acc > 2:
            dy = 1

        # This is where the player would like to be
        nx = player_x + dx
        ny = player_y + dy

        if nx >= 0 and nx < 16 and ny >= 0 and ny < 16 and m.get_cell(nx, ny) != 1:            
            # The requested room is valid. Erase the player from the last spot.
            neo[player_y*16+player_x] = (0,0,0)
            # Move the player and draw the new spot
            player_x, player_y = nx, ny    
            neo[player_y*16+player_x] = (0,0,50)
            neo.show()
            # Return if the player found the treasure
            if nx == treasure_x and ny == treasure_y:
                print("You found the treasure!")
                return
        
        # A bit of a delay to slow down the movement
        time.sleep(0.25)

while True:
    play()