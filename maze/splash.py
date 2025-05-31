from pixelgrid import PixelGrid
import time

TILT=b'\x01\x01\x01\x00\x02\x02\x02\x00\x03\x00\x00\x00\x04\x04\x04\x00\x00\x01\x00\x00\x00\x02\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x02\x02\x02\x00\x03\x03\x03\x00\x00\x04\x00\x00'
MAZE=b'\x01\x01\x00\x01\x01\x00\x02\x02\x02\x00\x03\x03\x03\x00\x04\x04\x01\x00\x01\x00\x01\x00\x02\x00\x02\x00\x00\x00\x03\x00\x04\x00\x01\x00\x01\x00\x01\x00\x02\x02\x02\x00\x00\x03\x00\x00\x04\x04\x01\x00\x00\x00\x01\x00\x02\x00\x02\x00\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\x01\x00\x02\x00\x02\x00\x03\x03\x03\x00\x04\x04'
HYPHEN_A=b'\x00\x00\x00\x03\x03\x03\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00\x01\x01\x00\x03\x03\x03\x00\x02\x02\x00\x00\x00\x03\x00\x03\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00'

SPLASH_COLORS = [
    # Mixed colors
    (0, 0, 0),   # 0
    (50, 0, 0),  # 1
    (0, 50, 0),  # 2
    (0, 0, 50),  # 3
    (0, 50, 50), # 4

    # Greens +5
    (0, 0, 0),   # 0
    (0, 50, 0),  # 1
    (0, 50, 0),  # 2
    (0, 50, 0),  # 3
    (0, 50, 0),  # 4

    # Blues +10
    (0, 0, 0),   # 0
    (0, 0, 50),  # 1
    (0, 0, 50),  # 2
    (0, 0, 50),  # 3
    (0, 0, 50),  # 4

    # Cyans +15
    (0, 50, 0),   # 0
    (0, 50, 50),  # 1
    (0, 50, 50),  # 2
    (0, 50, 50),  # 3
    (0, 50, 50),  # 4

]

def check_stop_delay(w,acc):    
    _,_, z = acc.acceleration
    if z<0:
        raise StopIteration("Stop signal received from accelerometer")
    time.sleep(w)


def splash_screen(neo,acc):

    # Wait for the board to be upright
    while True:
        _,_, z = acc.acceleration
        if z > 5:
            break

    neo.set_palette_colors(SPLASH_COLORS)
    scr = PixelGrid(16, 16)
    for i in range(17):
        scr.fill(0)  # Fill with black
        scr.draw_image(4,5,9,5,HYPHEN_A,15)
        scr.draw_image(i-16,0,16,4,TILT,5)        
        scr.draw_image(16-i,11,16,5,MAZE,10)
        neo.show(scr)
        check_stop_delay(0.05,acc)
    time.sleep(1)
    neo.set_palette_colors(SPLASH_COLORS)
    scr.draw_image(4,5,9,5,HYPHEN_A)
    scr.draw_image(i-16,0,16,4,TILT)        
    scr.draw_image(16-i,11,16,5,MAZE)
    neo.show(scr)
    for _ in range(16):
        a = neo.get_color(1)
        neo.set_color(1, neo.get_color(2))
        neo.set_color(2, neo.get_color(3))
        neo.set_color(3, neo.get_color(4))
        neo.set_color(4, a)
        neo.show(scr)
        check_stop_delay(0.1,acc)
    time.sleep(1)
    