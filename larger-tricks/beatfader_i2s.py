# beatfader_i2s.py -- fade between different drum loops
# 13 Dec 2022 - @todbot / Tod Kurt
#
# Tested on Lolin S2 Mini ESP32-S2 https://circuitpython.org/board/lolin_s2_mini/
#
# Copy this file to CIRCUITPY/code.py
# Copy the beatfader_wav dir to CIRCUITPY/beatfader_wav
#
# Wiring is:
# - Hook a PCM5102 I2S DAC to S2 Mini like:
#  - IO39 - BCK on PCM5102
#  - IO37 - LCLK on PCM5102
#  - IO35 - DIN on PCM5102
# - Hook up a potentiometer knob to IO3
# - That's it!
#

import time
import board
import analogio
import audiocore, audiomixer, audiobusio

wav_files = (
    # filename,                               loop?
    ('beatfader_wavs/amen_22k16b_160bpm.wav', True),
    ('beatfader_wavs/dnb21580_22k16b_160bpm.wav', True),
    ('beatfader_wavs/drumloopA_22k16b_160bpm.wav', True),
    ('beatfader_wavs/amen_22k16b_160bpm.wav', True),
)
num_voices = len(wav_files)

potknob = analogio.AnalogIn(board.IO3)

i2s_bclk = board.IO39  # BCK on PCM5102 I2S DAC (SCK pin to Gnd)
i2s_wsel = board.IO37  # LCLK on PCM5102
i2s_data = board.IO35  # DIN on PCM5102

audio = audiobusio.I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)

mixer = audiomixer.Mixer(voice_count=num_voices, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer)  # attach mixer to audio playback

for i in range(num_voices):
    (wav_file, loopit) = wav_files[i]
    wave = audiocore.WaveFile(open(wav_file,"rb"))
    mixer.voice[i].level = 0.0             # turn down volume
    mixer.voice[i].play(wave, loop=loopit) # start wav playing

n = num_voices * 0.8  # amount of overlap between samples
m  = 1/(num_voices-1) # size of slice

while True:
    potval = potknob.value
    frac = potknob.value / 65535
    for i in range(num_voices):
        l = min(max( 1 - (n * (frac - m*i))**2, 0), 1) # fancy math to for nice mixing
        mixer.voice[i].level = l
        print("%1.2f" % l, end=" ")
    print("%0.2f", frac)
    time.sleep(0.05)
