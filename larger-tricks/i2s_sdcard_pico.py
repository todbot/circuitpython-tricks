# i2s_sdcard_pico.py -- I2S Audio from SD Card on RP2040 Pico
# 20 May 2022 - @todbot / Tod Kurt

import time
import board, busio
import audiocore, audiomixer, audiobusio
import sdcardio, storage, os

# pin definitions
i2s_bclk = board.GP9  # BCK on PCM5102 (connect PCM5102 SCK pin to Gnd)
i2s_wsel = board.GP10 # LCK on PCM5102
i2s_data = board.GP11 # DIN on PCM5102
sd_mosi = board.GP19
sd_sck = board.GP18
sd_miso = board.GP16
sd_cs = board.GP17

# sd card setup
sd_spi = busio.SPI(clock=sd_sck, MOSI=sd_mosi, MISO=sd_miso)
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# audio setup
audio = audiobusio. I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

# find all WAV files on SD card
wav_fnames =[]
for filename in os.listdir('/sd'):
    if filename.lower().endswith('.wav') and not filename.startswith('.'):
        wav_fnames.append("/sd/"+filename)
wav_fnames.sort()  # sort alphanumerically for mixtape numbered order

print("found WAVs:")
for fname in wav_fnames:
    print("  ", fname)

while True:
    # play WAV file one after the other
    for fname in wav_fnames:
        print("playing WAV", fname)
        wave = audiocore.WaveFile(open(fname, "rb"))
        mixer.voice[0].play(wave, loop=False )
        time.sleep(3)  # let WAV play a bit
        mixer.voice[0].stop()
