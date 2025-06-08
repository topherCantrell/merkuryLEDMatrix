import wifi, socketpool
import hardware
import neo_frame
import pixelgrid

from tetris.network import TetrisNetwork

# The top panel is just a draw slave of the bottom panel. The top panel is in AP mode.
# The bottom panel is in station mode and connects to the top panel's wifi network.
# The top panel listens for UDP packets and draws images on the NeoPixels based on the 
# received data.

device = hardware.MerkuryHardware(use_nunchuk=False)

neo = neo_frame.NeoFrame(device.get_neo_pixels(), width=16, height=16)
# Initial colors
neo.set_palette_colors([
    [2,2,2],
    [0,50,0],
    [50,0,0]
])
pixels = pixelgrid.PixelGrid(width=16, height=16)
neo.show(pixels)

net = TetrisNetwork()

# Feedback that wifi is listening
for i in range(16):
    pixels.set_pixel(i, 0, 1)
neo.show(pixels)

net.start_top_network()

# Feedback that socket is ready
for i in range(16):
    pixels.set_pixel(i, 1, 1)
neo.show(pixels)

# Handle packets

# 1: set the color palette
# 1 nn (ii rr gg bb) ...

# 2: draw an image
# 2 xx yy ww hh po tr aa bb cc dd ...

while True:
    udp_buffer = net.receive_from_bottom()            
    if udp_buffer[0] == 1:
        # Set palette
        n = udp_buffer[1]        
        for i in range(n):
            ind = udp_buffer[2+i*4]
            neo.set_color(ind,[udp_buffer[2+i*4+1], udp_buffer[2+i*4+2], udp_buffer[2+i*4+3]])        
        neo.show(pixels)                
    elif udp_buffer[0] == 2:
        # Draw image
        x = udp_buffer[1]
        y = udp_buffer[2]
        w = udp_buffer[3]
        h = udp_buffer[4]
        po = udp_buffer[5]
        tr = udp_buffer[6]
        # print(f">>> image: {x},{y} {w}x{h} po={po} tr={tr} data={udp_buffer[7:7+w*h]}") 
        pixels.draw_image(x, y, w, h, udp_buffer[7:7+w*h], po, tr)        
        neo.show(pixels)       
        
