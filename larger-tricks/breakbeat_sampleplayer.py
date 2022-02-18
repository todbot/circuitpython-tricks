# breakbeat_sampleplayer.py -- play samples
#
# 8 Feb 2022 - @todbot / Tod Kurt
#
# Part of circuitpython-tricks: https://github.com/todbot/circuitpython-tricks
#
# For wiring diagram, see:
# https://github.com/todbot/circuitpython-tricks/larger-tricks/docs/breakbeat_sampleplayer_wiring.png
#
# Convert samples for use with SoX, like:
#  sox loop.mp3 -b 16 -c 1 -r 22050 loop.wav
#
# Or copy "breakbeat_wavs" folder as CIRCUITPY/wav
#

import random
import time
import board
import supervisor

import audiocore
import audiomixer
from audiopwmio import PWMAudioOut as AudioOut

import neopixel

leds = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

#def millis(): return supervisor.ticks_ms()  # I like millis
def millis(): return time.monotonic()*1000 # I like millis

wav_files = (
    # filename,           loop?
    ('wav/amenfull_22k_s16.wav', True), # 137.72 bpm
    ('wav/amen2_22k_s16.wav', False),
    ('wav/amen3_22k_s16.wav', False),
    ('wav/amen4_22k_s16.wav', False),
    ('wav/amen5_22k_s16.wav', False),
    ('wav/amen6_22k_s16.wav', False),
    ('wav/amen7_22k_s16.wav', False),
    ('wav/amen8_22k_s16.wav', False),
    ('wav/ohohoh2.wav', False),
)

# audio pin is RX (pin 1) (RP2040 GPIO1)
audio = AudioOut(board.RX)
mixer = audiomixer.Mixer(voice_count=len(wav_files), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
# attach mixer to audio playback
audio.play(mixer)

bpm = 137.72
beat_count = 4
millis_per_beat = 60_000 / bpm
millis_per_measure = millis_per_beat * beat_count
last_millis = 0
last_led_millis = 0

wav_num = 0
while True:
    leds[0] = 0x000000
    time.sleep(0.0001)
    now = millis()
    # a little blinky
    if now - last_led_millis >= millis_per_beat :
        last_led_millis = now
        leds[0] = 0x00ff00
        
    if now - last_millis >= millis_per_measure :
        last_millis = now
        print("playing wav", wav_num)
        leds[0] = 0xff00ff
        voice = mixer.voice[wav_num]
        (wav_file,loopit) = wav_files[wav_num]
        wave = audiocore.WaveFile(open(wav_file,"rb"))
        voice.play(wave,loop=loopit)
        # pick random for next time
        wav_num = random.randint(0,len(wav_files)-1)

        
