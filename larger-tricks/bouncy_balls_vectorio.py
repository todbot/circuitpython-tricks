# bouncy_balls_vectorio.py - use displayio to make simple bouncy balls
# 12 Nov 2024 - @todbot / Tod Kurt.  Based off bouncy_balls1.py
# video demo at https://gist.github.com/todbot/d216cdfd0c13774c713482395429da16
# works on any CircuitPython device with a display, just create a 'display'
import time, random
import board, busio, displayio, i2cdisplaybus
import vectorio
import adafruit_displayio_ssd1306

# configuration options
num_balls = 12
ball_size = 5
rand_vx, rand_vy = 2.5, 2
scl_pin, sda_pin = board.GP15, board.GP14    # pins your display is on
dw,dh = 128,64  # or whatever your display is

# set up the display (change for your setup)
displayio.release_displays()
disp_i2c = busio.I2C(scl=scl_pin, sda=sda_pin, frequency=400_000)
display_bus = i2cdisplaybus.I2CDisplayBus(disp_i2c, device_address=0x3C)  # or 0x3D 
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=dw, height=dh, rotation=180)

# set up the displayio objects that go on the display
maingroup = displayio.Group()
display.root_group = maingroup

# holder of x,y position and vx,vy velocity of a ball
# and the update method to update the position based on velocity
class Ball:
    def __init__(self,x,y, vx,vy, shape):
        self.x, self.y, self.vx, self.vy = x,y,vx,vy
        self.shape = shape
    def update(self):
        self.x = self.x + self.vx # update ball position
        self.y = self.y + self.vy # update ball position
        if self.x <= 0 or self.x > display.width:
            self.vx = -self.vx  # bounce!
        if self.y <= 0 or self.y > display.height:
            self.vy = -self.vy  # bounce!
        self.shape.x = int(self.x)
        self.shape.y = int(self.y)
        
ballgroup = displayio.Group() # group of ballshapes (will fill out later)
maingroup.append(ballgroup)  # add ballshapes to screen
pal = displayio.Palette(1)
pal[0] = 0xffffff   # only two colors in OLEDland: white & black

balls = []
for i in range(num_balls):
    # start in middle of screen
    x, y = display.width//2, display.height//2 
    # random initial velocity
    vx, vy = random.uniform(-rand_vx,rand_vx), random.uniform(-rand_vy,rand_vy) 
    ballshape = vectorio.Circle(pixel_shader=pal, radius=ball_size, x=x, y=y)
    balls.append( Ball(x,y, vx,vy, ballshape) )  # our perfect math balls
    ballgroup.append(ballshape)  # our actual drawn ball shapes
    
while True:
    for ball in balls:
        ball.update()
    time.sleep(0.01)

