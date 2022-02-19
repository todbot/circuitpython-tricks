# beatfader.py -- fade between different drum loops
# 18 Feb 2022 - @todbot / Tod Kurt
#
# Tested on Raspberry Pi Pico
#
# Copy this file to CIRCUITPY/code.py
# Copy the beatfader_wavs files to CIRCUITPY/wav
#
# Note: CircuitPython will hang or freeze sometimes with audiopwmio
#       especially if USB access is happening (e.g. saving files)
#       To minimize this, stop the program (Ctrl-C in REPL) before
#       saving.
#
# Circuit as in ./docs/breakbeat_sampleplayer.fzz
#

import time
import math
import board
import analogio
import audiocore
import audiomixer
from audiopwmio import PWMAudioOut as AudioOut

wav_files = (
    # filename,           loop?
    ('wav/amen_22k16b_160bpm.wav', True), 
    ('wav/dnb21580_22k16b_160bpm.wav', True), 
    ('wav/drumloopA_22k16b_160bpm.wav', True),
    ('wav/amen_22k16b_160bpm.wav', True), 
)

potknob = analogio.AnalogIn(board.A2)

time.sleep(3)

audio = AudioOut(board.GP1)
mixer = audiomixer.Mixer(voice_count=len(wav_files), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
# attach mixer to audio playback
audio.play(mixer)

for i in range(len(wav_files)):
    (wav_file,loopit) = wav_files[i]
    wave = audiocore.WaveFile(open(wav_file,"rb"))
    mixer.voice[i].level = 0.0
    mixer.voice[i].play(wave, loop=loopit)

top = 65535
cnt = len(wav_files)
n = cnt * 0.8  # amount of overlap
m  = 1/(cnt-1)

while True:
    potval = potknob.value
    f = potknob.value / 65535
    print("%5d: %0.2f" % (potval,f), end='  ')
    for i in range(cnt):
        l = min(max( 1 - (n * (f - m*i))**2, 0), 1)
        print("%1.2f" % l, end=" ")
        mixer.voice[i].level = l
    print()
    time.sleep(0.05)
