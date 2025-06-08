import hardware
import neo_frame
import pixelgrid
import time
from tetris.network import TetrisNetwork
from tetris import graphics
from tetris import splash
import random
import graphic_digits

net = TetrisNetwork()
net.start_bottom_network()

device = hardware.MerkuryHardware(use_nunchuk=True)
nunchuk = device.get_nunchuk()
neo = neo_frame.NeoFrame(device.get_neo_pixels(), width=16, height=16)

def can_draw_tetra(grid, x,y, data):
    for yy in range(4):
        ay = yy+y 
        for xx in range(4):
            ax = xx + x            
            d = data[yy*4+xx]
            if d!=0:
                # Not transparent
                d = grid.get_pixel(ax,ay)
                if d!=1 and d!=2: # Playfield is color 1 and 2                    
                    return False    
    return True

def delay_break(nunchuk, wait_time):
    for i in range(wait_time*10):
        c = nunchuk.buttons.C
        if c:
            raise StopIteration()
        time.sleep(.10)

def play_tetris(demo):

    while nunchuk.buttons.C:
        time.sleep(.1)

    score = 0

    # Initialize color palette on both panels    
    net.send_palette(graphics.palette)  # Send the palette to the top panel
    neo.set_palette_colors(graphics.palette)  # Set the palette for bottom panel
    
    board = pixelgrid.PixelGrid(16,32) # The game board
    board.draw_solid_rect(0,11,16,21,3) # Border of the board
    board.draw_solid_rect(3,6,10,5,1) # Top play area is black
    board.draw_solid_rect(3,11,10,19,2) # Most of the play area is faintly white

    # Draw the score
    if not demo:
        board.draw_solid_rect(0,0,16,5,0) # Clear the score area
        graphic_digits.draw_number_centered(board, score, 7, 0, palette_offset=3)    

    # Select and draw the first piece
    piece_count = 1
    pn = random.randint(0,6)   
    x,y,r = graphics.starts[pn]    
    erase_buffer = board.get_rect(x,y,4,4)
    board.draw_image(x,y,4,4,graphics.tetras[pn][r],6)
    
    # Select the next piece (we will show it when the current piece has fallen away)
    next_pn = random.randint(0,6)
    next_x, next_y, next_r = graphics.starts[next_pn]
    next_drawn = False        

    net.update_panels(board,neo)

    state_Z = nunchuk.buttons.Z # For debouncing rotation requests

    if demo:
        drop_time_reload = 5
        drop_time = drop_time_reload
    else:
        drop_time_reload = 50
        drop_time = drop_time_reload    
    
    while True:

        dirty = False

        # "Dirty" means that we need to update the panels at the bottom of this loop. 
        # We do all our drawing on the back buffer grid. Whenever the grid is different 
        # from the last time we drew it, we set dirty to True and update the panels.

        # Show the next piece when the current piece has fallen away
        if y > 9 and not next_drawn:
            next_erase_buffer = board.get_rect(next_x,next_y,4,4)
            board.draw_image(next_x,next_y,4,4,graphics.tetras[next_pn][next_r],6)
            next_drawn = True
            dirty = True

        # Check for user movement (left,right,down,rotate)       

        nx = x
        ny = y
        nr = r                
        
        if demo and y%5 == 0:           
            if random.randint(0,99) <= 10:
                nr = (r + 1)%4
        else:
            # Check for rotation request
            rot = nunchuk.buttons.Z
            if not rot:
                state_Z = False
            else:
                if rot and not state_Z:
                    nr = (r + 1)%4
                    state_Z = True

        # End check during waits, but let's check here too
        if nunchuk.buttons.C:
            raise StopIteration("End of game requested by player")
        
        if demo and y%5 == 2:
            v = False
            dv = random.randint(0,99)
            if dv < 75:
                ofs = (piece_count % 3)-1
                nx = x + ofs
        else:
            # Check for left/right movement
            h,v = nunchuk.joystick
            if h < 100:
                nx = x - 1
            elif h > 150:
                nx = x + 1            

        # Erase the piece while we move it
        board.draw_image(x,y,4,4, erase_buffer)

        if can_draw_tetra(board, nx,ny,graphics.tetras[pn][nr]):
            if x!=nx or r!=nr:
                # Update the left/right and the rotation if OK
                x = nx
                r = nr                
                dirty = True # The piece actually moved

        erase_buffer = board.get_rect(x,y,4,4)        
        board.draw_image(x,y,4,4,graphics.tetras[pn][r],6)

        # Now gravity moves the piece down

        # Right now, the piece is freely moving down. We will lock it to the board if it hits the bottom.
        # When it is locked, we check for solid rows and remove them.
        locked = False

        # Move the piece down (by request or by gravity). The user can skip the delay time for faster
        # falling by pressing down on the joystick.
        drop_time -= 1
        if drop_time <= 0 or v < 100:
            drop_time = drop_time_reload
            board.draw_image(x,y,4,4,erase_buffer) # Erase the piece in the old position
            # y = y + 1
            # dirty = True
            # If the piece can move, move it down
            if can_draw_tetra(board, x, y+1, graphics.tetras[pn][r]):
                y += 1
                dirty = True
                erase_buffer = board.get_rect(x,y,4,4)
                board.draw_image(x,y,4,4,graphics.tetras[pn][r],6)    
            else:                
                # Draw the piece on the board and trigger a check for solid rows
                board.draw_image(x,y,4,4,graphics.tetras[pn][r],6)                
                locked = True
                # Switch to the next piece
                pn, x,y,r = next_pn, next_x, next_y, next_r
                erase_buffer = next_erase_buffer
                # Select a new next piece
                piece_count += 1
                next_pn = random.randint(0,6)
                next_x, next_y, next_r = graphics.starts[next_pn]
                next_drawn = False        
                drop_time = 0 # Immediately move th next piece                                                

        # Remove solid rows        

        if locked:
            to_remove = []
            for ty in range(11,30):
                solid = True         
                # Check if the row is solid       
                for tx in range(3,13):
                    if board.get_pixel(tx,ty) == 2:
                        solid = False
                        break
                if solid:
                    to_remove.append(ty)
                    score += 1
                    if score%4==0:
                        drop_time_reload -= 1                        
                    # Show the row to be removed
                    for tx in range(3,13):
                        board.set_pixel(tx,ty,5)
                    dirty = True
            if to_remove:
                net.update_panels(board,neo)
                delay_break(nunchuk,0.5)
                for ty in to_remove:
                    # All rows above the removed row
                    dat = board.get_rect(3,11,10,ty-11)
                    # Move the block down one row
                    board.draw_image(3,12,10,ty-11,dat,trans=255)
                    # Blanks roll into the top row
                    board.draw_solid_rect(3,11,10,1,2)
                # Draw the score
                if not demo:
                    board.draw_solid_rect(0,0,16,5,0) # Clear the score area
                    graphic_digits.draw_number_centered(board, score, 7, 0, palette_offset=3)   
                net.update_panels(board,neo)
                # Hold the change for a bit
                delay_break(nunchuk,0.5)
                dirty = False                  

        # If any pieces are above the top of the board after a lock, we have a game over           

        if locked:
            for tx in range(3,13):
                if board.get_pixel(tx,10) != 1: # Top part of playfield
                    for ty in range(11,30):
                        for tx in range(3,13):
                            if board.get_pixel(tx,ty) != 1 and board.get_pixel(tx,ty) != 2:
                                # Not a playfield pixel
                                board.set_pixel(tx,ty,6)
                        net.update_panels(board,neo)                        
                    print("Game over")
                    delay_break(nunchuk,2)
                    return
                    
        # Update the panels if there were any changes to the grid
        if dirty:            
            net.update_panels(board,neo)        

while True:
    while True:
        try:
            splash.splash_screen(neo, net, nunchuk)
            play_tetris(demo=True)
        except StopIteration:
            # Player requested a game     
            print("Starting Tetris game")
            break
    try:
        play_tetris(demo=False)
    except StopIteration:
        # Player requested a stop (back to the top)
        print("Stopping Tetris game")