# sdcard_max_wavs_code.py -- Find out how many WAVs can play at once from SD card
# 30 Jul 2023 - @todbot / Tod Kurt
#
# Plays I2S Audio from SD Card. Finds all WAVs in dir,
# plays one after the other until CircuitPython crashes
# On RP2040 Pico, maximum number of usable WAVs is about 10, with crashing at 14
# Be sure to use fast SD card
# To use:
#  - Copy this file to CIRCUITPY drive
#  - Copy the "sine_wavs" folder to an SD card. It contains 25 WAV files of different pitched sine waves
#  - Adjust the pin definitions below to match your board
#  - Plug SD card into your setup
#  - Start up CircuitPython board, watch the REPL and listen to the audio output to see when things crash
#

import time
import board, busio
import audiocore, audiomixer, audiobusio
import sdcardio, storage, os

wavdir="/sd/sine_wavs" # where we put our WAV files (without the "SD"

# pin definitions
i2s_bclk = board.GP9  # BCK on PCM5102 (be sure to connect PCM5102 SCK pin to Gnd)
i2s_wsel = board.GP10 # LCK on PCM5102
i2s_data = board.GP11 # DIN on PCM5102
sd_mosi = board.GP19
sd_sck = board.GP18
sd_miso = board.GP16
sd_cs = board.GP17

# sd card setup
sd_spi = busio.SPI(clock=sd_sck, MOSI=sd_mosi, MISO=sd_miso)
sdcard = sdcardio.SDCard(sd_spi, sd_cs, baudrate=32_000_000)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# find all WAV files on SD card
wav_fnames =[]
for filename in os.listdir(wavdir):
    if filename.lower().endswith('.wav') and not filename.startswith('.'):
        wav_fnames.append(wavdir+"/"+filename)

wav_fnames.sort()  # sort alphanumerically for mixtape numbered order
print("found WAVs:")
for fname in wav_fnames:
    print("  ", fname)

# audio setup, voice count is max number of WAVs found
audio = audiobusio. I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)
mixer = audiomixer.Mixer(voice_count=len(wav_fnames), sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True, buffer_size=1024)
audio.play(mixer) # attach mixer to audio playback

wavs = []
for i in range(len(wav_fnames)):
    fname = wav_fnames[i]
    print('opening',fname)
    wave = audiocore.WaveFile(wav_fnames[i]) #, bytearray(1024)) # added max buffer, doesn't help on RP2040
    wavs.append(wave)

print("spi:", sd_spi.frequency)  # should be about 32 MHz

# play WAV file one after the other
while True:
    i=0
    for i in range(len(wav_fnames)):
        print("playing WAV", wav_fnames[i])
        mixer.voice[i].play(wavs[i], loop=True )
        time.sleep(2)  # let WAV play a bit
