
class PixelGrid:
    """Draw primitives on a rectuangular pixel grid.

    This object creates and manipulates a one dimensional array of bytes.
    Other objects use the "frame" field as needed.
    """

    def __init__(self, width, height):
        self.frame = bytearray(width*height)
        self.width = width
        self.height = height

    def set_pixel(self, x, y, color):
        """Set the pixel at (x,y) to color"""
        self.frame[y*self.width+x] = color

    def get_pixel(self, x, y):
        """Get the pixel at (x,y)"""
        return self.frame[y*self.width+x]

    def fill(self, color):
        """Fill the entire frame with the given color"""
        for i in range(self.width*self.height):
            self.frame[i] = color

    # def get_rect(self, x, y, width, height):
    #     data = [0]*(width*height)
    #     for j in range(height):
    #         ay = y+j            
    #         for i in range(width):
    #             ax = x+i                
    #             data[j*width+i] = self.frame[ay*self._width+ax]
    #     return data
    
    # def can_draw_four_by_four(self, x,y,width,height,data, trans=0):   
    #     for yy in range(height):
    #         ay = yy+y 
    #         for xx in range(width):
    #             ax = xx + x            
    #             d = data[yy*width+xx]
    #             if d!=trans:
    #                 # Not transparent
    #                 if self.frame[ay*self._width + ax] != trans:
    #                     return False
    #     return True

    # def draw_solid_rect(self, x, y, width, height, color):
    #     for j in range(height):
    #         ay = y+j
    #         if ay < 0 or ay >= self._height:
    #             continue
    #         for i in range(width):
    #             ax = x+i
    #             if ax < 0 or ax >= self._width:
    #                 continue
    #             self.frame[ay*self._width+ax] = color

    # def erase_rect(self, x,y,width,height, data, trans=0):
    #     for j in range(height):
    #         ay = y+j
    #         if ay < 0 or ay >= self._height:
    #             continue
    #         for i in range(width):
    #             ax = x+i
    #             if ax < 0 or ax >= self._width:
    #                 continue
    #             if data[j*width+i] != 0:
    #                 self.frame[ay*self._width+ax] = 0

    def draw_image(self, x, y, width, height, data, palette_offset=0, trans=0):
        for j in range(height):
            ay = y+j
            if ay < 0 or ay >= self.height:
                continue
            for i in range(width):
                ax = x+i
                if ax < 0 or ax >= self.width:
                    continue
                pv = data[j*width+i]
                if pv != trans:
                    self.frame[ay*self.width+ax] = pv + palette_offset

    
    