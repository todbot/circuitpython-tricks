# gc9a01_multi_eyeball_code.py --
# 14 Oct 2022 - @todbot / Tod Kurt
# Part of circuitpython-tricks/larger-tricks
# Requires rebuilt CircuitPython with CIRCUITPY_DISPLAY_LIMIT set to 3
# see: https://todbot.com/blog/2022/05/19/multiple-displays-in-circuitpython-compiling-custom-circuitpython/

import time, math, random
import board, busio
import displayio
import adafruit_imageload
import gc9a01

displayio.release_displays()

dw, dh = 240,240  # display dimensions

eyeball_bitmap, eyeball_pal = adafruit_imageload.load("imgs/eye0_ball2.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("imgs/eye0_iris0.bmp")
iris_pal.make_transparent(0)

iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw//2 - iris_w//2, dh//2 - iris_h//2

tft0_clk  = board.GP18
tft0_mosi = board.GP19

tft1_clk  = board.GP10
tft1_mosi = board.GP11

tft_L0_rst = board.GP21
tft_L0_dc  = board.GP22
tft_L0_cs  = board.GP20

tft_R0_rst = board.GP26
tft_R0_dc  = board.GP27
tft_R0_cs  = board.GP28

tft_L1_rst = board.GP14
tft_L1_dc  = board.GP12
tft_L1_cs  = board.GP13

tft_R1_rst = board.GP3
tft_R1_dc  = board.GP4
tft_R1_cs  = board.GP5

spi0 = busio.SPI(clock=tft0_clk, MOSI=tft0_mosi)
spi1 = busio.SPI(clock=tft1_clk, MOSI=tft1_mosi)

def eye_init(spi, dc, cs, rst, rot):
    display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=rst)
    display = gc9a01.GC9A01(display_bus, width=dw, height=dh, rotation=rot)
    main = displayio.Group()
    display.show(main)
    eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
    iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x = iris_cx, y = iris_cy )
    main.append(eyeball)
    main.append(iris)
    return (display, eyeball, iris)


(display_L0, eyeball_L0, iris_L0) = eye_init( spi0, tft_L0_dc, tft_L0_cs,  tft_L0_rst, rot=0)
(display_R0, eyeball_R0, iris_R0) = eye_init( spi0, tft_R0_dc, tft_R0_cs,  tft_R0_rst, rot=0)
(display_L1, eyeball_L1, iris_L1) = eye_init( spi1, tft_L1_dc, tft_L1_cs,  tft_L1_rst, rot=0)
# can't do four yet
#(display_R1, eyeball_R1, iris_R1) = eye_init( spi1, tft_R1_dc, tft_R1_cs,  tft_R1_rst, rot=0)

the_eyes = [
    #                                 x,y,             tx,ty, next_time
    [display_L0, eyeball_L0, iris_L0, iris_cx, iris_cy, 0, 0, 0 ],
    [display_R0, eyeball_R0, iris_R0, iris_cx, iris_cy, 0, 0, 0 ],
    [display_L1, eyeball_L1, iris_L1, iris_cx, iris_cy, 0, 0, 0 ],
    #[display_R1, eyeball_R1, iris_R1, iris_cx, iris_cy, 0, 0, 0 ],  # can't do four yet
]


r = 17  # allowable deviation from center for iris

while True:
    for i in range(len(the_eyes)):
        (display, eyeball, iris, x,y, tx,ty, next_time) = the_eyes[i]
        x = x * 0.5 + tx * 0.5  # "easing"
        y = y * 0.5 + ty * 0.5
        iris.x = int( x )
        iris.y = int( y )
        the_eyes[i][3] = x
        the_eyes[i][4] = y
        if time.monotonic() > next_time:
            next_time = time.monotonic() + random.uniform(0,2)
            tx = iris_cx + random.uniform(-r,r)
            ty = iris_cy + random.uniform(-r,r)
            the_eyes[i][5] = tx
            the_eyes[i][6] = ty
            the_eyes[i][7] = next_time  # FIXME
            print("change!")
        #display.refresh( target_frames_per_second=20 )
        display.refresh()
