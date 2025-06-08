import wifi, socketpool

class TetrisNetwork:

    def __init__(self):
        # For the top panel. This is the buffer we read into
        self.udp_buffer = bytearray(500)

    def start_top_network(self):
        # The top panel is in AP mode
        wifi.radio.start_ap('TopMat','TopMatPass')
        print("AP started with IP", wifi.radio.ipv4_address_ap)    

        # Create our listener socket
        pool = socketpool.SocketPool(wifi.radio)         
        self.sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM) # UDP socket
        self.sock.bind(('192.168.4.1', 1234))  # say we want to listen on this host,port

    def receive_from_bottom(self):
        # Clear any last command just in case
        self.udp_buffer[0] = 0
        size,addr = self.sock.recvfrom_into(self.udp_buffer)    
        # print(f"Received message from {addr}:{self.udp_buffer[:size]}")
        return self.udp_buffer

    def start_bottom_network(self):
        # The bottom panel is in station mode and connects to the top panel's wifi network
        wifi.radio.connect('TopMat','TopMatPass')
        pool = socketpool.SocketPool(wifi.radio)         
        self.sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM) # UDP socket

    def send_to_top(self, data):
        self.sock.sendto(bytearray(data), ('192.168.4.1',1234))

    # UDP command 1: set the color palette
    # 1 nn (ii rr gg bb) ...
    def send_palette(self, palette):
        pos = 0
        pal = []
        for color in palette:
            tp = [pos, color[0], color[1], color[2]]
            pal.append(tp)        
            pos += 1
        msg = [1, len(pal)]
        for c in pal:
            msg.extend([c[0], c[1], c[2], c[3]])  # n - r,g,b
        self.send_to_top(msg)    

    # UDP command 2: draw an image
    # 2 xx yy ww hh po tr aa bb cc dd ...
    def send_image(self, x, y, width, height, data, palette_offset=0, trans=0):
        msg = [2, x, y, width, height, palette_offset, trans]
        msg.extend(data)
        self.send_to_top(msg)

    def update_panels(self, board, neo):
        data = board.get_rect(0,0,16,16)
        self.send_image(0,0,16,16,data,0,255)
        neo.show_viewport(board, 0,16)
