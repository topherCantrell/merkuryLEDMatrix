import neopixel
import board
import time
import random
import busio
import adafruit_nunchuk

i2c = busio.I2C(board.GP13, board.GP12)
nc = adafruit_nunchuk.Nunchuk(i2c)

pixels = neopixel.NeoPixel(board.GP6, 256, auto_write=False)

pixels.fill((0, 0, 0))
pixels.show()

# import wifi
# wifi.radio.start_ap('TopMat','TopMatPass')

pal = [
    (0, 0, 0),
    (0, 50, 0),
    (0, 0, 50),
    (10, 50, 10),
    (50, 50, 50),
]

inv1 = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
    0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
    0, 0, 3, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 0, 0,
    0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
    0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 0, 0,
    0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

inv2 = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
    0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
    0, 0, 3, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 0, 0,
    0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
    0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 3, 3, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0,
    0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

invaders = [inv1, inv2]

def draw_frame(pal, data):
    for i in range(256):
        pixels[i] = pal[data[i]]
    pixels.show()


def four_by_four_trans(dest, data, x, y):
    for yy in range(16):
        ay = yy+y
        if ay < 0 or ay > 15:
            # Not visible
            continue
        for xx in range(16):
            ax = xx + x
            if ax < 0 or ax > 15:
                # Not visible
                continue
            d = data[yy*16+xx]
            if d:
                # Not transparent
                dest[ay*16 + ax] = d


MIN_X = -4
MIN_Y = -4
MAX_X = 4
MAX_Y = 4

x = 0
y = 0
inv = 0
dx = 1
dy = 1
while True:
    can = [0]*256
    four_by_four_trans(can, invaders[inv], x, y)
    # print(x, y, dx, dy, nc.joystick)
    draw_frame(pal, can)
    time.sleep(0.25)

    # Flip animation
    inv += 1
    inv = inv % 2

    if nc.buttons.Z:
        x,y = nc.joystick
        x = int(x / 16) - 8
        y = 16 - int(y / 16) - 8
        continue

    if x < MIN_X or x > MAX_X or y < MIN_Y or y > MAX_Y:
        # Time to change direction
        if x <= MIN_X:
            x = MIN_X
            while True:
                dx = random.choice([0, 1, 2])
                # dy = random.choice([-2, -1, 0, 1, 2])
                if dx or dy:
                    break
        if x >= MAX_X:
            x = MAX_X
            while True:
                dx = random.choice([0, -1, -2])
                # dy = random.choice([-2, -1, 0, 1, 2])
                if dx or dy:
                    break
        if y <= MIN_Y:
            y = MIN_Y
            while True:
                dy = random.choice([0, 1, 2])
                # dx = random.choice([-2, -1, 0, 1, 2])
                if dx or dy:
                    break
        if y >= MAX_Y:
            y = MAX_Y
            while True:
                dy = random.choice([0, -1, -2])
                # dx = random.choice([-2, -1, 0, 1, 2])
                if dx or dy:
                    break

    x = x + dx
    y = y + dy
