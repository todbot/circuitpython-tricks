# wavmix_s2mini_i2s_sd.py -- fade two WAV loops on ESP32-S2 mini w/ I2S DAC
# 17 Jul 2025 - @todbot / Tod Kurt
#
# Tested on Lolin S2 Mini ESP32-S2 https://circuitpython.org/board/lolin_s2_mini/
# video demo: https://www.youtube.com/watch?v=97OA6L9PLCg
#
# Copy this file to CIRCUITPY/code.py
# Make the directory "/mysd" on CIRCUITPY, but leave it empty
# Copy the "wavmix" dir to an SD card
#
# Wiring is:
# - Hook a PCM5102 I2S DAC to S2 Mini :
#  - IO39 - BCK on PCM5102
#  - IO37 - LCLK on PCM5102
#  - IO35 - DIN on PCM5102
#
# - Hook up SD card to S2 Mini:
#  - IO7  - SD card SCK
#  - IO9  - SD card MISO
#  - IO11 - SD card MOSI
#  - IO12 - SD card CS
#
# - Hook up potentiometer knob to IO3 
#

import os
import time
import board
import busio
import analogio
import sdcardio
import storage
import audiocore, audiomixer, audiobusio

time.sleep(3)  # let USB calm down

num_voices = 2  # how many WAVs to play simultaneously
sample_rate = 44100  
channel_count = 2  # stereo samples
sd_mount_point = "/mysd"  # make this directory in your CIRCUITPY drive, if not there

# pin definitions
i2s_bclk  = board.IO39  # BCK on PCM5102 I2S DAC (SCK pin to Gnd)
i2s_wsel  = board.IO37  # LCLK on PCM5102
i2s_data  = board.IO35  # DIN on PCM5102

sd_sck    = board.IO7   # "CLK"
sd_miso   = board.IO9   # "SO"
sd_mosi   = board.IO11  # "SI"
sd_cs     = board.IO12  # "CS"

knob1_pin = board.IO3

# set up pots (could extend this to more pots)
knob1 = analogio.AnalogIn(knob1_pin)

# set up audio
audio = audiobusio.I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)
mixer = audiomixer.Mixer(voice_count=num_voices, buffer_size=4096, sample_rate=sample_rate,
                         channel_count=channel_count, bits_per_sample=16, samples_signed=True)
audio.play(mixer)  # attach mixer to audio playback

# sd card setup
sd_spi = busio.SPI(clock=sd_sck, MOSI=sd_mosi, MISO=sd_miso)
sdcard = sdcardio.SDCard(sd_spi, sd_cs, baudrate=16_000_000)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, sd_mount_point)

# look for our WAV files
wav_filenames = []
for filename in os.listdir(sd_mount_point+"/wavmix"):
    if filename.lower().endswith('.wav') and not filename.startswith('.'):
        wav_filenames.append(sd_mount_point+"/wavmix/"+filename)    

# start playing the WAVs in sync, but at 0 level, use pots to control volume
for i in range(num_voices):
    wav_file = wav_filenames[i]
    print("playing wav:", wav_file)
    wave = audiocore.WaveFile(open(wav_file,"rb"))
    mixer.voice[i].level = 0.0            # turn down volume
    mixer.voice[i].play(wave, loop=True)   # start wav playing as a loop

while True:
    # set the volume of each voice based on knob position
    knobval = knob1.value / 54000   # should be 65535, ESP ADCs don't do full range
    mixer.voice[0].level = knobval
    mixer.voice[1].level = 1 - knobval
    print("knobval: %.2f" % knobval)
    time.sleep(0.1)

