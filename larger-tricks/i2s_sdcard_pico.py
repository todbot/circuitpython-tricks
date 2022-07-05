# i2s_sdcard_pico.py -- I2S Audio from SD Card on RP2040 Pico
# 20 May 2022 - @todbot / Tod Kurt

import time
import board, busio
import audiocore
import audiomixer
import audiobusio
import sdcardio, storage, os

# countdown delay to let us Ctrl-C if CirPy crashes b/c audio
for i in range(3): print("countdown", 3-i); time.sleep(1) 

# i2s_bclk = board.GP0  # SPI0 RX  / I2C0 SDA
# i2s_wsel = board.GP1  # SPI0 CS  / I2C0 SCL
# i2s_data = board.GP2  # SPI0 SCK / I2C1 SDA

i2s_bclk = board.GP9 
i2s_wsel = board.GP10
i2s_data = board.GP11 

# i2s_bclk = board.GP13  # doesn't work
# i2s_wsel = board.GP14
# i2s_data = board.GP15 

sd_clk   = board.GP18
sd_mosi  = board.GP19
sd_miso  = board.GP16
sd_cs    = board.GP17

num_voices = 3  #len(wav_files)

audio = audiobusio.I2SOut(bit_clock=i2s_bclk, word_select=i2s_wsel, data=i2s_data)

mixer = audiomixer.Mixer(voice_count=num_voices, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

sd_spi = busio.SPI(clock=sd_clk, MOSI=sd_mosi, MISO=sd_miso)

wav_files = []
sdcard = sdcardio.SDCard(sd_spi, cs=sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
for fn in os.listdir('/sd'):
    print("sd file:",fn)
    if fn.lower().endswith('.wav') and not fn.startswith('.'):
        wav_files.append("/sd/"+fn)
for f in wav_files:
    print("wav file:", f)



mixer.voice[0].level = 1.0
mixer.voice[1].level = 0.0
mixer.voice[2].level = 0.75

# this crashes the i2s with earsplitting demon hiss
#mixer.voice[0].play( audiocore.WaveFile(open(wav_files[0], "rb")), loop=True )
#mixer.voice[1].play( audiocore.WaveFile(open(wav_files[1], "rb")), loop=True )

wave0 = audiocore.WaveFile(open(wav_files[2], "rb"))
wave1 = audiocore.WaveFile(open(wav_files[1], "rb"))
wave2 = audiocore.WaveFile(open(wav_files[3], "rb"))
mixer.voice[0].play( wave0, loop=True )
mixer.voice[1].play( wave1, loop=True )
mixer.voice[2].play( wave2, loop=True )

# fade each channel up and down
up_down_inc = 0.03
while True:
    print("up_down_inc",up_down_inc)
    mixer.voice[1].level = min(max(mixer.voice[1].level + up_down_inc, 0), 1)
    mixer.voice[0].level = min(max(mixer.voice[0].level - up_down_inc, 0), 1)
    if mixer.voice[0].level == 0 or mixer.voice[1].level == 0:
        up_down_inc = -up_down_inc
    time.sleep(0.1)
