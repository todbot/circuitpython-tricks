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
        #eye.lid_up.y += 5
        #eye.lid_lo.y += 5



import time, random, board, audiobusio, audiomixer, synthio
import gc


synth = synthio.Synthesizer(channel_count=2, sample_rate=28000)
mixer = audiomixer.Mixer(channel_count=2, sample_rate=28000, buffer_size=2048)
audio = audiobusio.I2SOut(bit_clock=board.MOSI, word_select=board.MISO, data=board.SCK)

audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.15  # I'm on headphones so cut level a lot on PCM5102

synth.envelope = synthio.Envelope(sustain_level=0.6, attack_time=0.001, release_time=1.0)

print("todbot Hello World!")
#  hi 2_041_568

while True:
    print("hi", gc.mem_free())
    synth.press( (65,69,72) ) # midi notes 65,69,72  = F4, A4, C5
    time.sleep(0.5)
    synth.release( (65,69,72) )
    time.sleep(1.5)




# synthio_note_info_play.py - try out new "synth.note_info()" api
# 20 Jul 2023 - @todbot / Tod Kurt
# works on QTPy RP2040 ESP32-S2, ESP32-S3 w/ I2C DAC (PCM5102A module for instance)

import time, random, board, audiobusio, audiomixer, synthio

synth = synthio.Synthesizer(channel_count=2, sample_rate=28000)
mixer = audiomixer.Mixer(channel_count=2, sample_rate=28000, buffer_size=2048)
audio = audiobusio.I2SOut(bit_clock=board.MOSI, word_select=board.MISO, data=board.SCK)

amp_env = synthio.Envelope(sustain_level = 0.5, # 0.5 to give us headroom w/ squ waves
                           attack_time = 0.5,   # to let us see these phases
                           decay_time = 0.5,
                           release_time = 3)

audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.15  # I'm on headphones so cut level a lot on PCM5102

midi_note = 42
notes_pressed = []
last_press_time = 0
import gc
while True:
    time.sleep(0.05)
    #print("notes_pressed:\n", ''.join([f"\t{n}\n" for n in notes_pressed]))
    for n in notes_pressed:
        note_info = synth.note_info(n)   # NOTE: it takes a Note object
        #print( "\tnote_info", note_info )
        if note_info[0] is None:
            notes_pressed.remove(n)

    print("note:",midi_note)
    print("hi", gc.mem_free())

    if time.monotonic() - last_press_time >= 0.5:
        last_press_time = time.monotonic()

        note = synthio.Note( frequency=synthio.midi_to_hz(midi_note), envelope=amp_env )
        notes_pressed.append(note)
        synth.press(note)

        midi_note = midi_note + 4 if midi_note < 70 else 42

        # release a random note (after we have a few)
        if len(notes_pressed) > 2:
            r = random.randint(0, len(notes_pressed)-1)
            n = notes_pressed[r]
            synth.release( n )




# synthio_eighties_dystopia.py --
# 19 Jun 2023 - @todbot / Tod Kurt
# - A swirling ominous wub that evolves over time
# - Made for QTPy RP2040 but will work on any synthio-capable board
# - No user input, just wallow in the sound
# - video demo: https://youtu.be/EcDqYh-DzVA
#
# Circuit:
# - See: "eighties_arp_bb.png" wiring
# - QT Py RP2040 or similar
# - QTPy RX pin is audio out, going through RC filter (1k + 100nF) to TRS jack
#
# Code:
#  - Five detuned oscillators are randomly detuned very second or so
#  - A low-pass filter is slowly modulated over the filters
#  - The filter modulation rate also changes randomly every second (also reflected on neopixel)
#  - Every 15 seconds a new note is randomly chosen from the allowed note list

import time, random
import board, audiobusio, audiopwmio, audiomixer, synthio
import ulab.numpy as np
import neopixel, rainbowio   # circup install neopixel

notes = (33, 34, 31) # possible notes to play MIDI A1, A1#, G1
note_duration = 15   # how long each note plays for
num_voices = 5       # how many voices for each note
lpf_basef = 500      # filter lowest frequency
lpf_resonance = 1.5  # filter q

led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)

#audio = audiopwmio.PWMAudioOut(board.RX)  # RX pin on QTPY RP2040
#audio = audiobusio.I2SOut(bit_clock=board.MOSI, word_select=board.MISO, data=board.SCK)
audio = audiobusio.I2SOut(bit_clock=board.MOSI, word_select=board.MISO, data=board.SCK)

mixer = audiomixer.Mixer(channel_count=1, sample_rate=28000, buffer_size=2048)
synth = synthio.Synthesizer(channel_count=1, sample_rate=28000)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.2

# our oscillator waveform, a 512 sample downward saw wave going from +/-30k
wave_saw = np.linspace(30000, -30000, num=512, dtype=np.int16)  # max is +/-32k but gives us headroom
amp_env = synthio.Envelope(attack_level=0.8, sustain_level=0.8)

# set up the voices (aka "Notes" in synthio-speak) w/ initial values
voices = []
for i in range(num_voices):
    voices.append( synthio.Note( frequency=0, envelope=amp_env, waveform=wave_saw ) )

# set all the voices to the "same" frequency (with random detuning)
# zeroth voice is sub-oscillator, one-octave down
def set_notes(n):
    for voice in voices:
        #f = synthio.midi_to_hz( n ) + random.uniform(0,1.0)  # what orig sketch does
        f = synthio.midi_to_hz( n + random.uniform(0,0.4) ) # more valid if we move up the scale
        voice.frequency = f
    voices[0].frequency = voices[0].frequency/2  # bass note one octave down

# the LFO that modulates the filter cutoff
lfo_filtermod = synthio.LFO(rate=0.05, scale=2000, offset=2000)
# we can't attach this directly to a filter input, so stash it in the blocks runner
synth.blocks.append(lfo_filtermod)

note = notes[0]
last_note_time = time.monotonic()
last_filtermod_time = time.monotonic()

# start the voices playing
set_notes(note)
synth.press(voices)


while True:

    # continuosly update filter, no global filter, so update each voice's filter
    for v in voices:
        v.filter = synth.low_pass_filter( lpf_basef + lfo_filtermod.value, lpf_resonance )

    led.fill( rainbowio.colorwheel( lfo_filtermod.value/20 ) )  # show filtermod moving

    if time.monotonic() - last_filtermod_time > 1:
        last_filtermod_time = time.monotonic()
        # randomly modulate the filter frequency ('rate' in synthio) to make more dynamic
        lfo_filtermod.rate = 0.01 + random.random() / 8
        print("filtermod",lfo_filtermod.rate)

    if time.monotonic() - last_note_time > note_duration:
        last_note_time = time.monotonic()
        # pick new note, but not one we're currently playing
        note = random.choice([n for n in notes if n != note])
        set_notes(note)
        print("note", note, ["%3.2f" % v.frequency for v in voices] )
