
class PixelGrid:

    def __init__(self, width, height):
        self._frame = [0]*(width*height)
        self._width = width
        self._height = height

    def draw_pixel(self, x, y, color):
        self._frame[y*self._width+x] = color

    def get_pixel(self, x, y):
        return self._frame[y*self._width+x]

    def draw_fill(self, color):
        for i in range(self._width*self._height):
            self._frame[i] = color

    def get_rect(self, x, y, width, height):
        data = [0]*(width*height)
        for j in range(height):
            ay = y+j            
            for i in range(width):
                ax = x+i                
                data[j*width+i] = self._frame[ay*self._width+ax]
        return data
    
    def can_draw_four_by_four(self, x,y,width,height,data, trans=0):   
        for yy in range(height):
            ay = yy+y 
            for xx in range(width):
                ax = xx + x            
                d = data[yy*width+xx]
                if d!=trans:
                    # Not transparent
                    if self._frame[ay*self._width + ax] != trans:
                        return False
        return True

    def draw_solid_rect(self, x, y, width, height, color):
        for j in range(height):
            ay = y+j
            if ay < 0 or ay >= self._height:
                continue
            for i in range(width):
                ax = x+i
                if ax < 0 or ax >= self._width:
                    continue
                self._frame[ay*self._width+ax] = color

    def erase_rect(self, x,y,width,height, data, trans=0):
        for j in range(height):
            ay = y+j
            if ay < 0 or ay >= self._height:
                continue
            for i in range(width):
                ax = x+i
                if ax < 0 or ax >= self._width:
                    continue
                if data[j*width+i] != 0:
                    self._frame[ay*self._width+ax] = 0

    def draw_rect(self, x, y, width, height, data, palette_offset=0, trans=0):
        for j in range(height):
            ay = y+j
            if ay < 0 or ay >= self._height:
                continue
            for i in range(width):
                ax = x+i
                if ax < 0 or ax >= self._width:
                    continue
                if data[j*width+i] != trans:
                    self._frame[ay*self._width+ax] = data[j*width+i]+palette_offset