# vectorio_rotate_example.py
# 21 Jul 2022 - @todbot / Tod Kurt
# Rotation of a vectorio polygon

import time
import board
import displayio
import vectorio
import math

display = board.DISPLAY  # assume we have built-in display

#path0 = [(-20.0,-20.0), (-20.0,20.0), (20.0,20.0), (20.0,-20.0)]
path0_w = 50.000
path0_h = 50.000
path0 = [(26.000,1.003),(26.775,5.948),(27.548,10.879),(28.321,15.813),(31.002,13.640),(34.145,9.746),(37.280,5.861),(37.399,7.204),(35.601,11.864),(33.800,16.532),(34.700,18.496),(39.374,16.693),(44.044,14.891),(46.777,14.205),(42.882,17.349),(38.986,20.492),(35.380,23.553),(40.324,24.328),(45.260,25.101),(50.196,25.874),(46.855,26.649),(41.914,27.423),(36.972,28.198),(37.724,30.489),(41.619,33.633),(45.514,36.776),(45.548,37.689),(40.877,35.887),(36.226,34.093),(33.213,33.946),(35.016,38.619),(36.814,43.281),(38.300,47.402),(35.161,43.513),(32.021,39.623),(28.877,35.726),(27.799,39.514),(27.025,44.458),(26.251,49.400),(25.476,47.654),(24.703,42.719),(23.928,37.776),(22.016,37.098),(18.881,40.982),(15.738,44.877),(14.020,46.302),(15.821,41.634),(17.616,36.982),(18.802,32.924),(14.141,34.722),(9.477,36.522),(4.812,38.322),(7.861,35.666),(11.740,32.536),(15.629,29.397),(13.275,27.923),(8.334,27.149),(3.396,26.375),(3.535,25.603),(8.472,24.829),(13.411,24.056),(15.539,22.530),(11.641,19.384),(7.745,16.240),(4.933,13.725),(9.602,15.526),(14.266,17.326),(18.937,19.128),(17.570,14.898),(15.772,10.238),(13.970,5.569),(15.813,7.216),(18.954,11.108),(22.102,15.009),(23.951,14.082),(24.724,9.142),(25.497,4.212),]

shape0_w = 50  # not necessarily min/max of path
shape0_h = 50
shape0_color = 0xff00ff   # preferred color

### vectorio_tools

def rotate_points(pts, a):
    """Rotate a list of points pts by angle a around origin"""
    sa, ca = math.sin(a), math.cos(a)  # do this computation only once
    return [ (p[0]*ca - p[1]*sa, p[1]*ca + p[0]*sa) for p in pts ] # p[0]=x, p[1]=y

def recenter_points(pts, c=(0,0)):
    """Center points around new origin c"""
    return [(p[0] - c[0], p[1] - c[1]) for p in pts]

def rescale_points(pts, orig_w, orig_h, new_w, new_h):
    """Rescale point path to new w,h"""
    return [ (new_w * p[0] / orig_w, new_h * p[1] / orig_h ) for p in pts]

def int_points(pts):
    """Convert array of flooat points to int, for vectorio"""
    return [(int(p[0]),int(p[1])) for p in pts]

###

maingroup = displayio.Group()
display.root_group = maingroup # put main group on display, everything goes in maingroup

path0 = recenter_points(path0, c=(path0_w//2, path0_h//2))

# create vectorio shape, put in a group, put that on maingroup
pal = displayio.Palette(1)
pal[0] = shape0_color
shape0 = vectorio.Polygon(pixel_shader=pal, points=int_points(path0))
shapeg = displayio.Group()  #scale=1, x = 0, y=0)
shapeg.append(shape0)
maingroup.append(shapeg)

x,y = 80, 80  # starting location for our shape
theta = 0
xvel, yvel = 1.8, 1.0  # xy velocity
theta_vel = 0.04

last_time = 0
while True:

    elapsed_time = time.monotonic()

    # rotate about shape origin
    shape0.points = int_points( rotate_points(path0, theta) )

    elapsed_time = time.monotonic() - elapsed_time

    if time.monotonic() - last_time > 0.5:
        last_time = time.monotonic()
        print("elapsed millis %d" % (elapsed_time * 1000))

    # update position
    x,y = x + xvel, y + yvel
    theta = theta + theta_vel
    shapeg.x = int(x)
    shapeg.y = int(y)

    # bounce on screen edge hit
    if x < shape0_w//2 or x > (display.width - shape0_w//2):
        xvel = -xvel
    if y < shape0_h//2 or y > (display.height - shape0_h//2):
        yvel = -yvel

    time.sleep(0.05)
