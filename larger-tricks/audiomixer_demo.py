# audiomixer_demo.py -- show how to fade up and down playing loops
# note this causes glitches and crashes on RP2040
# 9 Feb 2022 - @todbot / Tod Kurt

import time
import board
import audiocore
import audiomixer
#from audiopwmio import PWMAudioOut as AudioOut  # for RP2040 etc
from audioio import AudioOut as AudioOut  # for SAMD51 etc

num_voices = 2

# audio pin is almost any pin on RP2040, let's do RX (pin 1) (RP2040 GPIO1)
# audio pin is A0 on SAMD51 (Trelllis M4, Itsy M4, etc)
audio = AudioOut(board.A0)
mixer = audiomixer.Mixer(voice_count=num_voices, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True)
# attach mixer to audio playback
audio.play(mixer)

mixer.voice[0].level = 1.0
mixer.voice[1].level = 0.0

# start drum loop playing
wave0 = audiocore.WaveFile(open("wav/drumsacuff_22k_s16.wav","rb"))
mixer.voice[0].play( wave0, loop=True )

# start synth loop playing
wave1 = audiocore.WaveFile(open("wav/snowpeaks_22k_s16.wav","rb"))
mixer.voice[1].play( wave1, loop=True )

time.sleep(1.0)  # let drums play a bit

while True:
    mixer.voice[1].level = min(max(mixer.voice[1].level + 0.01, 0), 1)
    mixer.voice[0].level = min(max(mixer.voice[0].level - 0.01, 0), 1)
    time.sleep(0.1)
