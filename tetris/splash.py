import pixelgrid
import time

palette = [
    (0,0,0),      # 0: Transparent
    (2,2,2),      # 1: Background
    #    
    (50,0,0),     # 2: T
    (0,50,0),     # 3: E
    (0,0,50),     # 4: T
    (50,50,0),    # 5: R
    (0,50,50),    # 6: I
    (50,0,50),    # 7: S
    (0,50,50),    # 8: U
    (1,1,1),
    (1,1,1),
    (1,1,1),
]

SPLASH = [
    bytes([ 
        1, 1, 1, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]),
    bytes([ 
        1, 1, 1, 0, 0,
        1, 0, 0, 0, 0,
        1, 1, 0, 0, 0,
        1, 0, 0, 0, 0,
        1, 1, 1, 0, 0,
    ]),
    bytes([ 
        1, 1, 0, 0, 0,
        1, 0, 1, 0, 0,
        1, 1, 0, 0, 0,
        1, 0, 1, 0, 0,
        1, 0, 1, 0, 0,
    ]),
    bytes([ 
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]),
    [
        bytes([
            0,1,1,1,0,
            0,1,0,0,0,
            0,1,1,1,0,
            0,0,0,1,0,
            0,1,1,1,0,
        ]),
        bytes([
            0,0,0,0,0,
            1,0,1,1,1,
            1,0,1,0,1,
            1,1,1,0,1,
            0,0,0,0,0,        
        ]),
    ],[
        bytes([        
            0,0,0,0,0,
            1,0,0,0,0,
            1,1,1,1,0,
            0,0,0,0,0,
            0,0,0,0,0,        
        ]),
        bytes([
            0,0,0,0,0,
            0,0,1,0,0,
            0,0,1,0,0,
            0,0,1,0,0,
            0,1,1,0,0,
        ]),
    ]
]

def delay_break(nunchuk, wait_time):
    for i in range(wait_time*10):
        c = nunchuk.buttons.C
        if c:
            raise StopIteration()
        time.sleep(.10)

def splash_screen(neo, net, nunchuk):
    while nunchuk.buttons.C:
        time.sleep(.1)
    board = pixelgrid.PixelGrid(16, 32)    
    board.fill(1) # Fill with background color    

    neo.set_palette_colors(palette)
    net.send_palette(palette)    
    net.update_panels(board, neo) # Clear the panels
    
    time.sleep(1)

    board.draw_image(0,0, 5,5, SPLASH[0], 1) # T
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)
    board.draw_image(1,5, 5,5, SPLASH[1], 2) # E
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)
    board.draw_image(2,11, 5,5, SPLASH[0], 3) # T
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)
    board.draw_image(3,16, 5,5, SPLASH[2], 4) # R
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)
    board.draw_image(3,22, 5,5, SPLASH[3], 5) # I
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)
    board.draw_image(4,27, 5,5, SPLASH[4][0], 6) # S
    net.update_panels(board, neo)
    delay_break(nunchuk,.5)

    frag_u_x = 9
    frag_u_y = -10

    frag_s_x = 9
    frag_s_y = -5    

    for i in range(33):
        frag_u_erase_buffer = board.get_rect(frag_u_x, frag_u_y, 5, 5)
        board.draw_image(frag_u_x, frag_u_y, 5, 5, SPLASH[5][0], 7)

        if i < 12:
            frag_s_rot = 1
        else:
            frag_s_rot = 0

        frag_s_erase_buffer = board.get_rect(frag_s_x, frag_s_y, 5, 5)        
        board.draw_image(frag_s_x, frag_s_y, 5, 5, SPLASH[4][frag_s_rot], 6)

        net.update_panels(board, neo)

        board.draw_image(frag_u_x, frag_u_y, 5, 5, frag_u_erase_buffer)
        board.draw_image(frag_s_x, frag_s_y, 5, 5, frag_s_erase_buffer)

        frag_u_y += 1
        frag_s_y += 1

        delay_break(nunchuk,.1)

    frag_s_y -= 1
    board.draw_image(frag_s_x, frag_s_y, 5, 5, SPLASH[4][frag_s_rot], 6)
    frag_u_y -= 2
    board.draw_image(frag_u_x, frag_u_y, 5, 5, SPLASH[5][1], 7)
    net.update_panels(board, neo)
    board.draw_image(frag_u_x, frag_u_y, 5, 5, frag_u_erase_buffer)
    delay_break(nunchuk,.1)

    for i in range(6):
        board.draw_image(frag_u_x, frag_u_y, 5, 5, SPLASH[5][1], 7)
        net.update_panels(board, neo)
        board.draw_image(frag_u_x, frag_u_y, 5, 5, frag_u_erase_buffer)
        delay_break(nunchuk,.1)
        frag_u_x -= 1

    delay_break(nunchuk,5)