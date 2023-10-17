# qteye_blink_esp32s3.py - a stand-alone GC9A01 round LCD "eye" on a QTPy ESP32-S3
# 16 Oct 2023 - @todbot / Tod Kurt
# Part of circuitpython-tricks/larger-tricks/eyeballs
# also see: https://todbot.com/blog/2022/05/19/multiple-displays-in-circuitpython-compiling-custom-circuitpython/

import time, math, random
import board, busio
import displayio
import adafruit_imageload
import gc9a01

# wiring for QT Py, should work on any QT Py or XIAO board, but ESP32-S3 is fastest
tft0_clk  = board.SCK
tft0_mosi = board.MOSI

tft_L0_rst = board.MISO
tft_L0_dc  = board.RX
tft_L0_cs  = board.TX

displayio.release_displays()

dw, dh = 240, 240  # display dimensions

# load our eye and iris bitmaps
eyeball_bitmap, eyeball_pal = adafruit_imageload.load("imgs/eye0_ball2.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("imgs/eye0_iris0.bmp")
iris_pal.make_transparent(0)
eyelid_bitmap = displayio.OnDiskBitmap(open("/imgs/eyelid_spritesheet2.bmp", "rb"))
eyelid_pal = eyelid_bitmap.pixel_shader
#eyelid_bitmap, eyelid_pal = adafruit_imageload.load("/imgs/eyelid_spritesheet.bmp")
eyelid_sprite_cnt = eyelid_bitmap.width // dw  # should be 16
eyelid_pal.make_transparent(1)

# compute or declare some useful info about the eyes
iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw//2 - iris_w//2, dh//2 - iris_h//2
r = 20  # allowable deviation from center for iris


spi0 = busio.SPI(clock=tft0_clk, MOSI=tft0_mosi)

# class to help us track eye info (not needed for this use exactly, but I find it interesting)
class Eye:
    def __init__(self, spi, dc, cs, rst, rot=0, eye_speed=0.25, twitch=2):
        display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=rst)
        display = gc9a01.GC9A01(display_bus, width=dw, height=dh, rotation=rot)
        display.auto_refresh = False
        main = displayio.Group()
        display.root_group = main
        self.display = display
        self.eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
        self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x=iris_cx,y=iris_cy)
        self.lids = displayio.TileGrid(eyelid_bitmap, pixel_shader=eyelid_pal, x=0, y=0, tile_width=dw, tile_height=dh)
        main.append(self.eyeball)
        main.append(self.iris)
        main.append(self.lids)
        self.x, self.y = iris_cx, iris_cy
        self.tx, self.ty = self.x, self.y
        self.next_time = time.monotonic()
        self.eye_speed = eye_speed
        self.twitch = twitch
        self.lidpos = 0
        self.lidpos_inc = 1
        self.lid_next_time = 0

    def update(self):
        # make the eye twitch around
        self.x = self.x * (1-self.eye_speed) + self.tx * self.eye_speed # "easing"
        self.y = self.y * (1-self.eye_speed) + self.ty * self.eye_speed
        self.iris.x = int( self.x )
        self.iris.y = int( self.y ) + 10
        if time.monotonic() > self.next_time:
            # pick a new "target" for the eye to look at
            t = random.uniform(0.25,self.twitch)
            self.next_time = time.monotonic() + t
            self.tx = iris_cx + random.uniform(-r,r)
            self.ty = iris_cy + random.uniform(-r,r)

        if time.monotonic() > self.lid_next_time:
            # make the eye blink its eyelids
            self.lid_next_time = time.monotonic() + random.uniform(1,3)
            self.lidpos = self.lidpos + self.lidpos_inc
            self.lids[0] = self.lidpos
            if self.lidpos == 0 or self.lidpos == eyelid_sprite_cnt-1:
                self.lidpos_inc *= -1  # change direction

        self.display.refresh()

# a list of all the eyes, in this case, only one
the_eyes = [
    Eye( spi0, tft_L0_dc, tft_L0_cs,  tft_L0_rst, rot=0),
]

while True:
    for eye in the_eyes:
        eye.update()

