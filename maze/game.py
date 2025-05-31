import random
import time
from maze import prim
from hardware import MerkuryHardware
from pixelgrid import PixelGrid
from neo_frame import NeoFrame
from maze import splash
import graphic_digits

device = MerkuryHardware()

neo = NeoFrame(device.get_neo_pixels())
acc = device.get_accelerometer()

GAME_COLORS = [
    (0, 0, 0),    # 0 Black
    (50, 0, 0),   # 1 Red
    (0, 50, 0),   # 2 Green
    (0, 0, 50),   # 3 Blue
    (50, 50, 0),  # 4 Yellow
    (50, 0, 50),  # 5 Magenta
    (0, 50, 50),  # 6 Cyan
    (50, 50, 50), # 7 White
]

class TiltPlayer:
    def __init__(self, acc):
        self.neo = neo
        self.acc = acc        

    def get_input(self, x, y, maze):
        """0=NONE, 1=UP, 2=RIGHT, 3=DOWN, 4=LEFT, 5=STOP"""
        # Read the accelerometer. Each axis is roughly -9.8 to 9.8.        
        y_acc, x_acc, _ = acc.acceleration                        
        
        # Simple input mapping here. If the accelerometer is tilted more than 2m/ss.
        
        if x_acc < -2:
            return 4  # LEFT
        if x_acc > 2:
            return 2 # RIGHT        
        if y_acc < -2:
            return 1 # UP
        if y_acc > 2:
            return 3 # DOWN
        
        return 0 # NONE, no movement detected

class DemoPlayer:

    DIRECTIONS = [
        (0,-1),  # UP
        (1,0),   # RIGHT
        (0,1),   # DOWN
        (-1,0)   # LEFT
    ]

    def __init__(self):
        self.current_direction = 0  # Start with UP
        self.wait_first_count = 5

    def turn(self,cw):
        if cw:
            self.current_direction = (self.current_direction + 1)
            if self.current_direction >= len(self.DIRECTIONS):
                self.current_direction = 0
        else:
            self.current_direction = (self.current_direction - 1)
            if self.current_direction < 0:
                self.current_direction = len(self.DIRECTIONS) - 1
    
    def look(self, x, y, maze):
        """Look in the current direction and return the pixel value"""
        dx, dy = self.DIRECTIONS[self.current_direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.width and 0 <= ny < maze.height:
            return maze.get_pixel(nx, ny)
        return 1 # Out of bounds, return wall  
        
    def get_input(self, x, y, maze):
        if self.wait_first_count > 0:
            self.wait_first_count -= 1
            return 0 # Wait for a few turns before starting to move
        # If the cell to the left is empty, turn left and move
        # Turn right until the cell in front is empty and move
        self.turn(False) # To the left
        val = self.look(x, y, maze) # Look left        
        if val == 1:  # If the left cell is a wall
            while self.look(x, y, maze) == 1:  # While the cell in front is a wall                
                self.turn(True) # Turn right
        return self.current_direction + 1  # Return the direction to move (1=UP, 2=RIGHT, 3=DOWN, 4=LEFT)

def delay_break(wait_time):
    for i in range(wait_time*10):
        _, _, z = acc.acceleration
        if z < 0:
            raise StopIteration()
        time.sleep(.10)

def play(width,height, player):    

    # Wait for the board to be upright
    while True:
        _,_, z = acc.acceleration
        if z > 5:
            break

    neo.set_palette_colors(GAME_COLORS)

    # Get a random maze wall color
    r,g,b = random.randint(0,100), random.randint(0,100), random.randint(0,100)
    neo.set_color(1, (r,g,b))
    
    # Generate a random maze
    maze = PixelGrid(width, height)
    prim.generate(maze)    
    
    # Add a yellow treasure to the maze
    treasure_x, treasure_y = random.randint(0,width-1), random.randint(0,height-1)
    while maze.get_pixel(treasure_x, treasure_y) != 0:
        treasure_x, treasure_y = random.randint(0,width-1), random.randint(0,height-1)        
    maze.set_pixel(treasure_x, treasure_y, 4)    

    # Add the blue player to the maze
    player_x, player_y = random.randint(0,width-1), random.randint(0,height-1)
    while maze.get_pixel(player_x, player_y) != 0:
        player_x, player_y = random.randint(0,width-1), random.randint(0,height-1)           

    while True:

        # Tilt way over to start/stop the game
        _, _, z_acc = acc.acceleration
        if z_acc < 0:
            raise StopIteration("Player requested a stop")

        # Get player input
        inp = player.get_input(player_x, player_y, maze)        

        dx, dy = 0,0
        # 0=NONE, 1=UP, 2=RIGHT, 3=DOWN, 4=LEFT, 5=STOP
        if inp == 1:
            dx,dy = 0,-1  # UP
        elif inp == 2:
            dx,dy = 1,0 # RIGHT
        elif inp == 3:
            dx,dy = 0,1 # DOWN
        elif inp == 4:
            dx,dy = -1,0 # LEFT            

        # This is where the player would like to move to
        nx = player_x + dx
        ny = player_y + dy

        if nx >= 0 and nx < width and ny >= 0 and ny < height and maze.get_pixel(nx, ny) != 1:                        
            # Move the player and draw the new spot
            player_x, player_y = nx, ny                            
            # Return if the player found the treasure
            if nx == treasure_x and ny == treasure_y:
                for i in range(16):
                    if i%2 == 0:
                        maze.set_pixel(player_x, player_y, 3)                
                    else:
                        maze.set_pixel(player_x, player_y, 4)     
                    neo.show_viewport(maze, player_x-7, player_y-7, 0)    
                    delay_break(.1)      
                return
            
        maze.set_pixel(player_x, player_y, 3)
        neo.show_viewport(maze, player_x-7, player_y-7, 0)        
        maze.set_pixel(player_x, player_y, 0)
        
        # A bit of a delay to slow down the movement
        delay_break(0.25)

# For feedback when the panel is turned over (start/stop)
solid = PixelGrid(16, 16)
solid.fill(100)

score_grid = PixelGrid(16, 16)
score_x_offests = [6, 4, 2, 0]

def show_score(score):
    score_grid.fill(0)  # Clear the score grid
    # Draw the score on the grid
    xo = score_x_offests[len(str(score)) - 1]  # Offset based on the number of digits
    graphic_digits.draw_number(score_grid, score, xo, 5, 3)
    neo.show(score_grid)

while True:
    # splash screen and demo loop
    while True:
        try:
            splash.splash_screen(neo, acc)
            play(8,8,DemoPlayer())
        except StopIteration:
            # Player requested a game            
            neo.set_color(100, (0,50,0))
            neo.show(solid)
            break
    
    # Player progresses through levels
    sz = 8
    num_treasures = 0
    while True:
        try:        
            play(sz, sz, TiltPlayer(acc))
            num_treasures += 1
            # Show the score
            show_score(num_treasures)
            delay_break(2)  # Wait for a bit before the next level
        except StopIteration:
            # Player requested a stop (back to the top)
            neo.set_color(100, (50,0,0))
            neo.show(solid)
            break
        sz += 2
        if sz > 64:
            sz = 64
