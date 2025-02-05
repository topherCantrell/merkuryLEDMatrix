import wifi, socketpool
from neo_frame import NeoFrame

# The top panel is just a draw slave of the bottom panel. The top panel is in AP mode.
# The bottom panel is in station mode and connects to the top panel.

# NeoPixels
neo = NeoFrame()
neo.set_palette_colors([
    [2,2,2],
    [0,50,0],
    [50,0,0]
])
neo.show()

# Start the network
wifi.radio.start_ap('TopMat','TopMatPass')
print("AP started with IP", wifi.radio.ipv4_address_ap)

# Feedback that network is ready
for i in range(16):
    neo.draw_pixel(i, 0, 1)
neo.show()

# Create our listener socket
pool = socketpool.SocketPool(wifi.radio)
udp_buffer = bytearray(500) 
sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM) # UDP socket
sock.bind(('192.168.4.1', 1234))  # say we want to listen on this host,port

# Feedback that socket is ready
for i in range(16):
    neo.draw_pixel(i, 1, 1)
neo.show()

# Handle packets

while True:
    udp_buffer[0] = 0
    size, addr = sock.recvfrom_into(udp_buffer)    
    # print(f"Received message from {addr}:{udp_buffer[:size]}")    
    if udp_buffer[0] == 1:
        # Set palette
        n = udp_buffer[1]
        pal = []
        for i in range(n):
            pal.append([udp_buffer[2+i*3], udp_buffer[3+i*3], udp_buffer[4+i*3]])
        neo.set_palette_colors(pal)
        neo.show()        
        # print(f">>> palette: {pal}")
    elif udp_buffer[0] == 2:
        # Draw image
        x = udp_buffer[1]
        y = udp_buffer[2]
        w = udp_buffer[3]
        h = udp_buffer[4]
        po = udp_buffer[5]
        trans = udp_buffer[6]
        neo.draw_rect(x, y, w, h, udp_buffer[7:7+w*h], palette_offset=po, trans=trans)
        neo.show()       
        # print(f">>> image: {x},{y} {w}x{h} {udp_buffer[5:5+w*h]}") 
