
class NeoFrame:

    def __init__(self, neo, width=16, height=16):          
        self._palette = [(0,0,0)]*256
        self._neo = neo
        self.width = width
        self.height = height

        # Set some default colors
        self.set_color(0, (0, 0, 0))    # Black
        self.set_color(1, (50, 0, 0))   # Red
        self.set_color(2, (0, 50, 0))   # Green
        self.set_color(3, (0, 0, 50))   # Blue
        self.set_color(4, (50, 50, 0))  # Yellow
        self.set_color(5, (50, 0, 50))  # Magenta
        self.set_color(6, (0, 50, 50))  # Cyan
        self.set_color(7, (50, 50, 50)) # White

    def set_palette_colors(self, palette, start=0):
        for c in palette:
            if start>=256:
                break
            self._palette[start] = c
            start += 1        

    def set_color(self, index, color):
        self._palette[index] = color

    def get_color(self, index):
        return self._palette[index]

    def show_viewport(self, pixelgrid, vx=0, vy=0, background=0):
        """Show the current viewport on the NeoPixels"""
        frame = pixelgrid.frame
        for j in range(16):
            for i in range(16):
                x = vx + i
                y = vy + j
                if x < 0 or x >= pixelgrid.width or y < 0 or y >= pixelgrid.height:
                    self._neo[j*16+i] = self._palette[background]
                else:
                    self._neo[j*16+i] = self._palette[frame[y*pixelgrid.width+x]]
        self._neo.show()

    def show(self, pixelgrid):
        """Fast show for grids that match the NeoPixel size"""
        frame = pixelgrid.frame
        for j in range(16):
            for i in range(16):
                self._neo[j*16+i] = self._palette[frame[j*self.width+i]]        
        self._neo.show()
    