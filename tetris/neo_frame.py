import neopixel
import board
from pixelgrid import PixelGrid

class NeoFrame(PixelGrid):

    def __init__(self, width=16, height=16):
        super().__init__(width, height)        
        self._palette = [(0,0,0)]*256
        self._neo = neopixel.NeoPixel(board.GP6, 256, auto_write=False)
        self._neo.fill((0,0,0))
        self._neo.show()

    def set_palette_colors(self, palette, start=0):
        for c in palette:
            if start>=256:
                break
            self._palette[start] = c
            start += 1        

    def set_color(self, index, color):
        self._palette[index] = color

    def show(self):
        for j in range(16):
            for i in range(16):
                self._neo[j*16+i] = self._palette[self._frame[j*self._width+i]]        
        self._neo.show()
    