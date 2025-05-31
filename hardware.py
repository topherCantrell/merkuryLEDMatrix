import neopixel
import board
import busio
import adafruit_nunchuk
import adafruit_mpu6050 


class MerkuryHardware:

    def __init__(self):

        # Strand of 256 neopixels on pin GP6
        self._neo_pixels = neopixel.NeoPixel(board.GP6, 256, auto_write=False)
        self._neo_pixels.fill((0, 0, 0))
        self._neo_pixels.show()

        # MPU6050 accelerometer on an I2C bus 1: GP15 and GP14
        self._acc_i2c = busio.I2C(board.GP15, board.GP14)
        self._mpu = adafruit_mpu6050.MPU6050(self._acc_i2c)

        # Nunchuk on I2C bus 0: GP1 and GP0
        # It might be plugged in later, so we don't create it yet
        self._nc_i2c = busio.I2C(board.GP1, board.GP0)
        self._nunchuk = None       

    def get_neo_pixels(self):
        """return the neopixels object

        You can do things like:
        ret.fill((0, 0, 10))
        ret.show()
        ret[0] = (10, 10, 10)        
        """        
        return self._neo_pixels
    
    def get_accelerometer(self):        
        """return the accelerometer object
        You can do things like:
        
        ret.acceleration
        """       
        return self._mpu
    
    def get_nunchuk(self):
        """return the nunchuk object
        You can do things like:
        ret.joystick
        ret.joystick.x
        ret.joystick.y
        ret.buttons
        """
        if self._nunchuk is None:
            try:
                self._nunchuk = adafruit_nunchuk.Nunchuk(self._nc_i2c)
            except Exception:
                print("Nunchuk not found")
                self._nunchuk = None                
        return self._nunchuk
    
