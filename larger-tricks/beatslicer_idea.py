# beatslicer_idea.py -- ideas on doing beatslicer on Trellis M4
# 24 Feb 2022 - @todbot / Tod Kurt

import time
import board
import audiocore
import audiomixer
from audioio import AudioOut as AudioOut 
import adafruit_trellism4

time.sleep(2)  # to give us time for when it crashes

# loop files must be tempo-sync'd!
# loops from https://github.com/todbot/circuitpython-tricks/tree/main/larger-tricks/beatfader_wavs
loop_files = (
    "wav/amen_22k16b_160bpm.wav", # mono 160 bpm
    "wav/dnb21580_22k16b_160bpm.wav", # mono 160 bpm
    "wav/drumloopA_22k16b_160bpm.wav", # mono 160 bpm
    "wav/femvoc_330662_22k16b_160bpm.wav", # mono 160 bpm
)
bpm = 160.00

# loop files must be tempo-sync'd!
# loop_files_old = (
#     "wav/drumsacuff_22k_s16.wav", # mono, bpm 137.72 (matches amen break)
#     "wav/drumsacuff_22k_s16.wav", # mono, bpm 137.72 (matches amen break)
#     "wav/drumsacuff_22k_s16.wav", # mono, bpm 137.72 (matches amen break)
#     "wav/snowpeaks_22k_s16.wav"
# )
# bpm_old = 137.72

num_loops = len(loop_files)
num_slices = 8

millis_per_beat = 60_000 / bpm
millis_per_measure = millis_per_beat * num_slices

trellis = adafruit_trellism4.TrellisM4Express(rotation=0)

# audio pin is almost any pin on RP2040, let's do A0 (RP2040 GPIO226) or RX (pin 1) (RP2040 GPIO1)
# audio pin is A0 and A1 on SAMD51 (Trelllis M4, Itsy M4, etc)
audio = AudioOut(board.A0)
#audio = AudioOut(left_channel=board.A1, right_channel=board.A0)
mixer = audiomixer.Mixer(voice_count=num_loops, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

# start drum loop playing, but silently
for i in range(num_loops):
    wave = audiocore.WaveFile(open(loop_files[i],"rb"))
    mixer.voice[i].play( wave, loop=True )
    mixer.voice[i].level = 0.0

def millis(): return time.monotonic()*1000 # I like millis

loop_slices = [[False] * num_loops for i in range(num_slices)]  # four loops with 8 sections
beat_pos = 0
last_led_millis = 0
current_press = set()

while True:
    # handle keypresses
    pressed = set(trellis.pressed_keys)
    for press in pressed - current_press:  # this is dumb
        x, y = press
        if not loop_slices[x][y]:
            loop_slices[x][y] = True
            trellis.pixels[x,y] = 0xff00ff # more responsive UI
        else:
            loop_slices[x][y] = False
            trellis.pixels[x,y] = 0x000000 # more responsive UI
    current_press = pressed
        
    now = millis()
    if now - last_led_millis >= millis_per_beat :
        last_led_millis = now
        print("beat:", beat_pos)

        # update mixer volumes
        for i in range(num_loops):    # rows
            if loop_slices[ beat_pos ][i]:
                mixer.voice[i].level = 1.0
            else:
                mixer.voice[i].level = 0.0

        # update LEDs
        # show which slices are selected
        for x in range(num_slices):
            for y in range(num_loops):
                if loop_slices[x][y]:
                    trellis.pixels[x,y] = 0xff00ff
                else: 
                    trellis.pixels[x,y] = 0x000000
        # set beat marker
        for i in range(num_loops):
            trellis.pixels[beat_pos,i] = 0x333333

        # go to next slice
        beat_pos = (beat_pos+1) % num_slices
    

