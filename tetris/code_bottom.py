import board
# import digitalio
import busio
import adafruit_nunchuk
import time
import wifi, socketpool
import time
from neo_frame import NeoFrame
import graphics
from pixelgrid import PixelGrid
import random

# NES controller
# latch = digitalio.DigitalInOut(board.GP18)
# latch.direction = digitalio.Direction.OUTPUT
# latch.value = False
# clock = digitalio.DigitalInOut(board.GP17)
# clock.direction = digitalio.Direction.OUTPUT
# clock.value = False
# data = digitalio.DigitalInOut(board.GP16)
# data.direction = digitalio.Direction.INPUT

# Nunchuk controller
i2c = busio.I2C(board.GP13, board.GP12)

# Same API as pixelgrid.set_palette_colors
def send_palette(pal):
    msg = [1, len(pal)]
    for c in pal:
        msg.extend(c)
    sock.sendto(bytearray(msg), ('192.168.4.1',1234))

# Same API as pixelgrid.draw_rect
def send_image(x, y, width, height, data, palette_offset=0, trans=0):
    msg = [2, x, y, width, height, palette_offset, trans]
    msg.extend(data)
    sock.sendto(bytearray(msg), ('192.168.4.1',1234))

def play_tetris():

    board = PixelGrid(16,34)
    board.draw_solid_rect(0,10,3,34,8)  # Left border
    board.draw_solid_rect(0,6,3,4,10) # Invisible border
    board.draw_solid_rect(13,10,3,34,8) # Right border
    board.draw_solid_rect(13,6,3,4,10) # Invisible border
    board.draw_solid_rect(0,33,16,1,8)  # Bottom border

    # Draw the score
    board.draw_rect(4,0,4,5,graphics.numbers[1],2)
    board.draw_rect(8,0,4,5,graphics.numbers[2],2)
    board.draw_rect(12,0,4,5,graphics.numbers[3],2)

    # Select and draw the first piece
    pn = random.randint(0,6)    
    x,y,r = graphics.starts[pn]    
    board.draw_rect(x,y,4,4,graphics.tetras[pn][r])

    # Select the next piece
    next_pn = random.randint(0,6)
    next_x, next_y, next_r = graphics.starts[next_pn]
    next_drawn = False    

    # Game board is a rect starting at (0,10) width=20, height=23

    score = 0
    graphics.draw_number(board, 0, 0, score)

    update_panels(board)

    state_Z = nun.buttons.Z
    drop_time_reload = 50
    drop_time = drop_time_reload
    
    while True:

        nx = x
        ny = y
        nr = r
        dirty = False

        # Show the next piece when the current piece has fallen away
        if y > 10 and not next_drawn:
            board.draw_rect(next_x,next_y,4,4,graphics.tetras[next_pn][next_r])
            next_drawn = True
            dirty = True
        
        # Check for rotation request
        rot = nun.buttons.Z
        if not rot:
            state_Z = False
        else:
            if rot and not state_Z:
                nr = (r + 1)%4
                state_Z = True    

        # Check for left/right movement
        h,v = nun.joystick
        if h < 100:
            nx = x - 1
        elif h > 150:
            nx = x + 1            

        # Can we rotate or left/right the piece?
        board.erase_rect(x,y,4,4,graphics.tetras[pn][r])
        if board.can_draw_four_by_four(nx,ny,4,4,graphics.tetras[pn][nr]):
            if x!=nx or r!=nr:            
                # Update the left/right and the rotation if OK
                x = nx
                r = nr
                dirty = True        

        # Right now, the piece is freely moving down. We will lock it to the board if it hits the bottom.
        locked = False

        # Move the piece down (by request or by gravity)        
        drop_time -= 1
        if drop_time <= 0 or v < 100:
            drop_time = drop_time_reload
            y = y + 1
            dirty = True
            # Check if the piece has locked to the board (hit bottom)
            if not board.can_draw_four_by_four(x,y,4,4,graphics.tetras[pn][nr]):
                board.draw_rect(x,y-1,4,4,graphics.tetras[pn][r])
                # Not dirty -- this is where the piece was before
                locked = True
                # Switch to the next piece and select a new next piece
                pn, x,y,r = next_pn, next_x, next_y, next_r
                next_pn = random.randint(0,6)
                next_x, next_y, next_r = graphics.starts[next_pn]
                next_drawn = False                                
                # Check for game over
                for tx in range(3,13):                
                    if board.get_pixel(tx,9) != 0:
                        print("Game over")
                        return                
        
        # Draw the tetra in old or new position
        board.draw_rect(x,y,4,4,graphics.tetras[pn][r])    

        # Check for solid rows and remove them
        if locked:
            to_remove = []
            for ty in range(10,33):
                solid = True                
                for tx in range(3,13):
                    if board.get_pixel(tx,ty) == 0:
                        solid = False
                        break
                if solid:
                    to_remove.append(ty)
                    score += 1
                    if score%4==0:
                        drop_time_reload -= 1
                        print(">>> reload",drop_time_reload)
                    for tx in range(3,13):
                        board.draw_pixel(tx,ty,11)
                    dirty = True
            if to_remove:
                update_panels(board)
                time.sleep(0.5)
                for ty in to_remove:
                    dat = board.get_rect(3,10,10,ty-10)
                    board.draw_rect(3,11,10,ty-10,dat,trans=255)
                    board.draw_rect(3,10,10,1,[0]*10)
                graphics.draw_number(board, 0, 0, score)
                update_panels(board)
                time.sleep(0.5)
                dirty = False
                
                    
                    
        if dirty:
            update_panels(board)        

def update_panels(board):
    # Draw top
    send_image(0,0,16,16,board.get_rect(0,0,16,16),trans=255)  # trans=255: ignore transparent
    # Draw bottom
    neo.draw_rect(0,0,16,16,board.get_rect(0,18,16,16),trans=255)  # trans=255: ignore transparent
    neo.show()  

#     
# Connect to the top panel
#

neo = NeoFrame()
neo.set_palette_colors([
    [2,2,2],
    [0,50,0],
    [50,0,0],
    [30,30,0]
])
neo.show()

progress = 0
while True:
    try:
        for i in range(16):
            neo.draw_pixel(i, 0, 0)
            neo.draw_pixel(i, 1, 0)
        for i in range(16):
            neo.draw_pixel(i, progress, 3)
        neo.show()
        progress = (progress + 1) % 2
        wifi.radio.connect('TopMat','TopMatPass')
        break
    except Exception:
        time.sleep(1)

# Feedback that network is ready
for i in range(16):
    neo.draw_pixel(i, 0, 1)
    neo.draw_pixel(i, 1, 0)
neo.show()

progress = 0
while True:
    try:
        for i in range(16):
            neo.draw_pixel(i, 2, 0)
            neo.draw_pixel(i, 3, 0)
        for i in range(16):
            neo.draw_pixel(i, progress+2, 3)
        neo.show()
        progress = (progress + 1) % 2
        nun = adafruit_nunchuk.Nunchuk(i2c)
        nun.joystick
        print(dir(nun))
        break
    except Exception:
        time.sleep(1)

# Feedback that nunchuck is ready
for i in range(16):
    neo.draw_pixel(i, 2, 1)
    neo.draw_pixel(i, 3, 0)
neo.show()

pool = socketpool.SocketPool(wifi.radio)
udp_buffer = bytearray(500) 
sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM) # UDP socket

# Feedback that socket is ready
for i in range(16):
    neo.draw_pixel(i, 1, 1)
neo.show()

# Clear the top display with black (not transparent)
send_palette(graphics.palette)
send_image(0,0,16,16,[0]*256,trans=255)

# Clear our display with black (not transparent)
neo.set_palette_colors(graphics.palette)
neo.draw_fill(0)
neo.show()

play_tetris()