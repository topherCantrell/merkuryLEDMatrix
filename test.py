import neopixel
import board
neo = neopixel.NeoPixel(board.GP6, 256, auto_write=False)
neo.fill((0,0,10))
neo.show()

import board
import busio
import adafruit_mpu6050
acc_i2c = busio.I2C(board.GP15, board.GP14)
mpu = adafruit_mpu6050.MPU6050(acc_i2c)
print(mpu.acceleration)

#    Y          X         Z (relative to display)
# (0.296881, -0.275333, 9.39006)  Screen up            +Z pointing down
# (0.739808, -0.146046, -10.6135) Screen down          -Z pointing down
#
# (10.2544, -0.280122, -0.622493) Standing on bottom   +Y pointing down
# (-9.27274, -0.25618, -1.13964)  Standing on top      -Y pointing down
# (0.390255, -10.0533, -1.02951)  Standing on left     -X pointing down 
# (0.411803, 9.54089, -0.94571)   Standing on right    +x poingint down

import board
import busio
nun = busio.I2C(board.GP1, board.GP0)
nun.try_lock()
nun.scan()

import time
while True:
    y_acc, x_acc, z_acc = mpu.acceleration
    x_acc = int((x_acc+10) * (16/20))
    y_acc = int((y_acc+10) * (16/20))
    neo.fill((0,0,0))
    neo[y_acc*16+x_acc] = (0,0,10)
    neo.show()
    time.sleep(0.1)
