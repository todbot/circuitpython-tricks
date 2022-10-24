# qteye_person_sensor.py -- quick hacking of Person Sensor by Useful Sensors onto qteye
# 23 Oct 2022 - @todbot / Tod Kurt
# Part of circuitpython-tricks/larger-tricks/eyeballs
# For more information on Person Sensor:
# https://github.com/usefulsensors/person_sensor_docs/blob/main/README.md
# https://github.com/usefulsensors/person_sensor_screen_lock
# https://www.hackster.io/petewarden/auto-lock-your-laptop-screen-with-a-person-sensor-7e0a35

import time, math, random, struct
import board, busio
import displayio
import adafruit_imageload
import gc9a01

displayio.release_displays()

debug_face = True

dw, dh = 240,240  # display dimensions

eyeball_bitmap, eyeball_pal = adafruit_imageload.load("imgs/eye0_ball2.bmp")
iris_bitmap, iris_pal = adafruit_imageload.load("imgs/eye0_iris0.bmp")
iris_pal.make_transparent(0)

iris_w, iris_h = iris_bitmap.width, iris_bitmap.height  # iris is normally 110x110
iris_cx, iris_cy = dw//2 - iris_w//2, dh//2 - iris_h//2
r = 20  # allowable deviation from center for iris

tft0_clk  = board.SCK
tft0_mosi = board.MOSI

tft_L0_rst = board.MISO
tft_L0_dc  = board.RX
tft_L0_cs  = board.TX

spi0 = busio.SPI(clock=tft0_clk, MOSI=tft0_mosi)

class Eye:
    def __init__(self, spi, dc, cs, rst, rot=0, eye_speed=0.25, twitch=2):
        display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=rst)
        display = gc9a01.GC9A01(display_bus, width=dw, height=dh, rotation=rot)
        main = displayio.Group()
        display.show(main)
        self.display = display
        self.eyeball = displayio.TileGrid(eyeball_bitmap, pixel_shader=eyeball_pal)
        self.iris = displayio.TileGrid(iris_bitmap, pixel_shader=iris_pal, x = iris_cx, y = iris_cy )
        main.append(self.eyeball)
        main.append(self.iris)
        self.x, self.y = iris_cx, iris_cy
        self.tx, self.ty = self.x, self.y
        self.next_time = time.monotonic()
        self.eye_speed = eye_speed
        self.twitch = twitch

    def update(self, do_random=False, ntx=None, nty=None):
        self.x = self.x * (1-self.eye_speed) + self.tx * self.eye_speed # "easing"
        self.y = self.y * (1-self.eye_speed) + self.ty * self.eye_speed
        self.iris.x = int( self.x )
        self.iris.y = int( self.y )

        if ntx is not None and nty is not None:
            self.tx = iris_cx + ntx
            self.ty = iris_cx + nty
        else:
            if do_random and time.monotonic() > self.next_time:
                t = random.uniform(0.25,self.twitch)
                self.next_time = time.monotonic() + t
                self.tx = iris_cx + random.uniform(-r,r)
                self.ty = iris_cy + random.uniform(-r,r)
                print("change!",t )
        self.display.refresh()

the_eye =  Eye( spi0, tft_L0_dc, tft_L0_cs,  tft_L0_rst, rot=0)

# The person sensor has the I2C ID of hex 62, or decimal 98.
PERSON_SENSOR_I2C_ADDRESS = 0x62

# We will be reading raw bytes over I2C, and we'll need to decode them into
# data structures. These strings define the format used for the decoding, and
# are derived from the layouts defined in the developer guide.
PERSON_SENSOR_I2C_HEADER_FORMAT = "BBH"
PERSON_SENSOR_I2C_HEADER_BYTE_COUNT = struct.calcsize(
    PERSON_SENSOR_I2C_HEADER_FORMAT)

PERSON_SENSOR_FACE_FORMAT = "BBBBBBbB"
PERSON_SENSOR_FACE_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_FACE_FORMAT)

PERSON_SENSOR_FACE_MAX = 4
PERSON_SENSOR_RESULT_FORMAT = PERSON_SENSOR_I2C_HEADER_FORMAT + \
    "B" + PERSON_SENSOR_FACE_FORMAT * PERSON_SENSOR_FACE_MAX + "H"
PERSON_SENSOR_RESULT_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_RESULT_FORMAT)

# How long to pause between sensor polls.
PERSON_SENSOR_DELAY = 0.3

# How large a face needs to be to count.
MAIN_FACE_MIN_WIDTH = 16  # was 32
MAIN_FACE_MIN_HEIGHT = 16

i2c = board.STEMMA_I2C()

# Wait until we can access the bus.
while not i2c.try_lock():
    pass

last_person_sensor_time = 0
# Keep looping and reading the person sensor results.
def get_faces():
    global last_person_sensor_time

    if time.monotonic() - last_person_sensor_time < PERSON_SENSOR_DELAY:
        return []
    last_person_sensor_time = time.monotonic()

    read_data = bytearray(PERSON_SENSOR_RESULT_BYTE_COUNT)
    i2c.readfrom_into(PERSON_SENSOR_I2C_ADDRESS, read_data)

    offset = 0
    (pad1, pad2, payload_bytes) = struct.unpack_from(
        PERSON_SENSOR_I2C_HEADER_FORMAT, read_data, offset)
    offset = offset + PERSON_SENSOR_I2C_HEADER_BYTE_COUNT

    (num_faces) = struct.unpack_from("B", read_data, offset)
    num_faces = int(num_faces[0])
    offset = offset + 1

    faces = []
    for i in range(num_faces):
        (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id,
         is_facing) = struct.unpack_from(PERSON_SENSOR_FACE_FORMAT, read_data, offset)
        offset = offset + PERSON_SENSOR_FACE_BYTE_COUNT
        face = {
            "box_confidence": box_confidence,
            "box_left": box_left,
            "box_top": box_top,
            "box_right": box_right,
            "box_bottom": box_bottom,
            "id_confidence": id_confidence,
            "id": id,
            "is_facing": is_facing,
        }
        faces.append(face)
    checksum = struct.unpack_from("H", read_data, offset)

    has_main_face = False
    has_lookie_loo = False
    for face in faces:
        width = face["box_right"] - face["box_left"]
        height = face["box_bottom"] - face["box_top"]
        big_enough_face = (
            width > MAIN_FACE_MIN_WIDTH and height > MAIN_FACE_MIN_HEIGHT)
        if big_enough_face:
            if not has_main_face:
                has_main_face = True
            else:
                if face["is_facing"] and face["box_confidence"] > 90:
                    has_lookie_loo = True

    if debug_face: print("faces:",faces)
    return faces

def map_range(s, a1, a2, b1, b2):
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

while True:
    faces = []
    faces = get_faces()

    facex, facey = None,None
    if len(faces) > 0:
        facex0 = (faces[0]['box_right'] - faces[0]['box_left']) // 2 + faces[0]['box_left']
        facex = map_range(facex0, 0,255, 30,-30)
        facey = 0
        print("facex: ",facex0,facex)

    the_eye.update( ntx=facex, nty=facey )
