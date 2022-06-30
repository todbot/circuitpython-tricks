# dvdlogo_vectorio_code.py - Bouncing DVD logo in CircuitPython vectorio
# 25 Mar 2022 - @todbot / Tod Kurt
# a vectorio rethink of https://github.com/todbot/circuitpython_screensaver
# video in action: https://twitter.com/todbot/status/1507516909528358916?s=21
# use https://shinao.github.io/PathToPoints/ to get a list of points
# then https://gist.github.com/todbot/05d8e64ba8c6a7a584c1956c817a8779 to normalize those points (see below)

import time
import board
import displayio
import vectorio
import rainbowio

class DVDLogo:
    def make_logo(width, height, color=0xFFFFFF, x=0, y=0):
        """ make a vectorio based DVD logo """
        pal = displayio.Palette(1)
        pal[0] = color
        points0 = []
        for i in range(len(DVDLogo.path0)):
            (dx,dy) = DVDLogo.path0[i]
            dx = int(dx * width)
            dy = int(dy * height)
            points0.append( (dx,dy) )
        dvdlogo0 = vectorio.Polygon(pixel_shader=pal, points=points0, x=x, y=y)
        
        points1 = []
        for i in range(len(DVDLogo.path1)):
            (dx,dy) = DVDLogo.path1[i]
            dx = int(dx * width)
            dy = int(dy * height)
            points1.append( (dx,dy) )
        dvdlogo1 = vectorio.Polygon(pixel_shader=pal, points=points1, x=x, y=y)
        
        dvdlogo = displayio.Group()
        dvdlogo.append(dvdlogo0)
        dvdlogo.append(dvdlogo1)
        return dvdlogo

    def change_color(logogroup, color):
        """ change color of logo, convenience function """
        logogroup[0].pixel_shader[0] = color
        
    # vector paths from SVG at https://upload.wikimedia.org/wikipedia/commons/9/9b/DVD_logo.svg
    # normalized to 1.0 on both x & y, original aspect ratio is 2:1
    path0 = (
    (0.580, 0.214), (0.550, 0.297), (0.521, 0.382), (0.509, 0.325), (0.494, 0.225), (0.479, 0.125), (0.455, 0.050), (0.406, 0.050), (0.358, 0.050), (0.309, 0.050), (0.260, 0.050), (0.211, 0.050), (0.162, 0.050), (0.114, 0.050), (0.098, 0.141), (0.132, 0.167), (0.181, 0.167), (0.230, 0.168), (0.276, 0.197), (0.301, 0.282), (0.285, 0.380), (0.246, 0.440), (0.198, 0.463), (0.160, 0.448), (0.171, 0.345), (0.182, 0.243), (0.152, 0.210), (0.103, 0.210), (0.083, 0.288), (0.072, 0.391), (0.061, 0.493), (0.057, 0.583), (0.106, 0.583), (0.155, 0.583), (0.203, 0.581), (0.252, 0.566), (0.298, 0.532), (0.340, 0.481), (0.376, 0.409), (0.398, 0.316), (0.397, 0.212), (0.403, 0.214), (0.419, 0.314), (0.435, 0.413), (0.451, 0.512), (0.467, 0.612), (0.483, 0.703), (0.515, 0.624), (0.547, 0.544), (0.579, 0.465), (0.611, 0.385), (0.643, 0.306), (0.675, 0.226), (0.712, 0.168), (0.760, 0.167), (0.809, 0.167), (0.857, 0.179), (0.896, 0.238), (0.897, 0.340), (0.865, 0.419), (0.820, 0.457), (0.772, 0.465), (0.766, 0.392), (0.777, 0.289), (0.774, 0.210), (0.725, 0.210), (0.688, 0.241), (0.677, 0.344), (0.666, 0.446), (0.655, 0.549), (0.684, 0.583), (0.733, 0.583), (0.782, 0.583), (0.830, 0.575), (0.877, 0.550), (0.922, 0.507), (0.961, 0.445), (0.990, 0.361), (1.000, 0.259), (0.981, 0.163), (0.943, 0.098), (0.898, 0.063), (0.849, 0.050), (0.800, 0.050), (0.752, 0.050), (0.703, 0.050), (0.654, 0.050), (0.619, 0.112), (0.588, 0.194), )
    path1 = (
    (0.485, 0.709), (0.436, 0.710), (0.387, 0.712), (0.339, 0.716), (0.290, 0.722), (0.241, 0.730), (0.193, 0.741), (0.145, 0.756), (0.097, 0.775), (0.050, 0.805), (0.031, 0.877), (0.075, 0.919), (0.123, 0.942), (0.171, 0.958), (0.220, 0.970), (0.268, 0.980), (0.317, 0.987), (0.366, 0.992), (0.414, 0.995), (0.463, 0.997), (0.512, 0.996), (0.561, 0.995), (0.6909, 0.991), (0.658, 0.986), (0.707, 0.979), (0.755, 0.969), (0.804, 0.957), (0.852, 0.940), (0.899, 0.916), (0.943, 0.870), (0.916, 0.802), (0.869, 0.773), (0.821, 0.754), (0.773, 0.740), (0.725, 0.730), (0.676, 0.722), (0.627, 0.716), (0.578, 0.712), (0.530, 0.709), (0.465, 0.904), (0.416, 0.897), (0.369, 0.871), (0.397, 0.820), (0.446, 0.808), (0.494, 0.809), (0.543, 0.821), (0.565, 0.874), (0.518, 0.898), (0.469, 0.904), )


display = board.DISPLAY

maingroup = displayio.Group()
display.show(maingroup) # put main group on display, everything goes in maingroup

dvdlogo_w = 80
dvdlogo_h = 40
x = 0 
y = 0 
xvel = 1.9
yvel = 1.4

dvdlogo = DVDLogo.make_logo( dvdlogo_w, dvdlogo_h, color=0xFF00FF, x=x,y=0 )
maingroup.append(dvdlogo) # put the logo on the display via the main group

while True:
  x = x + xvel
  y = y + yvel
  # if we hit an edge, bounce & change color!
  if x < 0 or x > (display.width - dvdlogo_w):
      xvel = -xvel
      DVDLogo.change_color(dvdlogo, rainbowio.colorwheel(time.monotonic()*50))
  if y < 0 or y > (display.height - dvdlogo_h):
      yvel = -yvel
      DVDLogo.change_color(dvdlogo, rainbowio.colorwheel(time.monotonic()*50))
  
  dvdlogo.x = int(x)
  dvdlogo.y = int(y)

  time.sleep(0.01)

